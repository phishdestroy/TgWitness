import asyncio
import copy
import secrets
import time
from itertools import groupby
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictInt, model_validator
from telethon import utils
from telethon.errors import RPCError, SlowModeWaitError
from telethon.tl import functions, types

from . import interactions, tuning
from .telegram_client import FLOOD_ERRORS

JOB = 'history_forward.job'
PLAN = 'history_forward.plan'
BUSY = 'This account is busy. Pause its current task before another Telegram operation.'
UNCERTAIN_CREATE = 'Creation outcome unknown. Check Telegram before starting another transfer.'
UNCERTAIN_SEND = 'Message outcome unknown. Review the destination before resuming.'
PROTECTED = 'Forwarding is restricted in this chat.'
DESTINATION = 'Choose a channel or group where this account can post.'
TERMINAL = {'completed', 'cancelled'}
ITEM_ERRORS = {'MessageIdInvalidError', 'MsgIdInvalidError', 'MediaEmptyError', 'BroadcastPublicVotersForbiddenError'}


class ForwardPlan(BaseModel):
    model_config = ConfigDict(extra='forbid')
    source: StrictInt = Field(ge=-(2**53-1), le=2**53-1)
    mode: Literal['channel', 'group', 'existing']
    destination: StrictInt | None = Field(default=None, ge=-(2**53-1), lt=0)
    title: str = Field(default='', max_length=128)

    @model_validator(mode='after')
    def valid(self):
        self.title = self.title.strip()
        if not self.source or self.mode == 'existing' and (self.destination is None or self.destination == self.source):
            raise ValueError(DESTINATION)
        if self.mode != 'existing' and (not self.title or self.destination is not None):
            raise ValueError('Enter a title for the new channel or group.')
        return self


class ForwardStart(BaseModel):
    model_config = ConfigDict(extra='forbid')
    plan_id: str = Field(pattern=r'^[a-f0-9]{32}$')
    request_id: str = Field(pattern=r'^[a-f0-9]{32}$')


class HistoryForward:
    def __init__(self, collector, lock):
        self.collector, self.store, self.lock = collector, collector.store, lock
        self.task = None
        self.job = self.store.get_setting(JOB, None)
        if self.job and self.job['state'] not in TERMINAL:
            if self.job.get('creating'):
                self.job.update(state='creation_unknown', error=UNCERTAIN_CREATE)
            elif self.job.get('pending', {}).get('dispatched'):
                self.job.update(state='uncertain', error=UNCERTAIN_SEND)
            else:
                self.job.update(state='paused', error=None)
            self.save()

    def save(self, event=None, details=None):
        try:
            with self.store.transaction():
                self.store.set_setting(JOB, self.job)
                if event:
                    self.store.append('interaction.forward.' + event, {'job_id': self.job['id'], 'destination': self.job.get('destination'),
                        'forwarded': self.job['forwarded'], 'skipped': self.job['skipped'], **(details or {})},
                        self.job['source'], actor_id=self.job['account_id'])
        except BaseException:
            self.job = self.store.get_setting(JOB, None)
            raise

    def status(self):
        if not self.job:
            return {'job': None}
        return {'job': copy.deepcopy({key: value for key, value in self.job.items()
            if key not in {'pending', 'creating', 'request', 'account_id', 'create_due'}})}

    def account(self):
        account = (self.store.get_setting('account', {}) or {}).get('id')
        if not account:
            raise ValueError('No Telegram account is connected.')
        return account

    async def source(self, chat_id):
        entity = await self.collector.resolve_target(chat_id)
        entity = await self.collector.client.get_entity(entity)
        if getattr(entity, 'noforwards', False):
            raise ValueError(PROTECTED)
        return entity

    async def destination(self, chat_id):
        entity = await self.collector.resolve_target(chat_id)
        entity = await self.collector.client.get_entity(entity)
        if not isinstance(entity, (types.Channel, types.Chat)) or any(getattr(entity, key, False) for key in ('left', 'deactivated', 'forum', 'monoforum')):
            raise ValueError(DESTINATION)
        permission = await self.collector.client.get_permissions(entity, 'me')
        if permission.is_creator:
            return entity
        if isinstance(entity, types.Channel) and entity.broadcast:
            if not permission.post_messages:
                raise ValueError(DESTINATION)
        elif not permission.is_admin:
            if permission.has_left:
                raise ValueError(DESTINATION)
            for rights in [getattr(entity, 'default_banned_rights', None), getattr(permission.participant, 'banned_rights', None)]:
                if rights and any(getattr(rights, key, False) for key in ('view_messages', 'send_messages', 'send_plain')):
                    raise ValueError(DESTINATION)
        return entity

    async def plan(self, body):
        interactions.permitted(self.collector)
        owner = 'forward-preview:' + secrets.token_hex(16)
        if not self.collector.reserve_export(owner):
            raise ValueError(BUSY)
        try:
            await self.collector.restore()
            account = self.account()
            source = await self.source(body.source)
            latest = await self.collector.client.get_messages(source, limit=1)
            if not latest:
                raise ValueError('No messages to export.')
            destination = await self.destination(body.destination) if body.mode == 'existing' else None
            plan = {'id': secrets.token_hex(16), **body.model_dump(), 'account_id': account,
                'source_title': utils.get_display_name(source), 'destination_title': utils.get_display_name(destination) if destination else body.title,
                'upper_id': latest[0].id, 'expires_at': time.time() + 600,
                'message_seconds': tuning.value(self.store, 'action_message_seconds'),
                'messages_per_hour': tuning.value(self.store, 'action_messages_per_hour')}
            self.store.set_setting(PLAN, plan)
            return {key: value for key, value in plan.items() if key != 'account_id'}
        except (*FLOOD_ERRORS, SlowModeWaitError) as exc:
            self.backoff(exc)
            raise
        finally:
            self.collector.release_export(owner)

    async def start(self, body, authorized):
        if self.job and self.job['id'] == body.request_id:
            if self.job['request'] != body.model_dump():
                raise ValueError('This request ID belongs to another action.')
            return self.status()
        if self.job and self.job['state'] not in TERMINAL:
            raise ValueError(BUSY)
        plan = self.store.get_setting(PLAN, None)
        if not plan or plan['id'] != body.plan_id or plan['expires_at'] < time.time() or plan['account_id'] != self.account():
            raise ValueError('This preview expired. Preview the transfer again.')
        if plan.get('started_job_id'):
            raise ValueError('This request ID belongs to another action.')
        authorized()
        interactions.permitted(self.collector)
        if not self.collector.reserve_export('forward:' + body.request_id):
            raise ValueError(BUSY)
        try:
            self.job = {**plan, 'id': body.request_id, 'request': body.model_dump(), 'cursor': 0,
                'state': 'running', 'forwarded': 0, 'skipped': 0, 'pending': {}, 'creating': False,
                'wait_until': None, 'error': None, 'recent_skips': [], 'created_at': time.time()}
            with self.store.transaction():
                self.save('started', {'upper_id': plan['upper_id'], 'mode': plan['mode']})
                self.store.set_setting(PLAN, {**plan, 'started_job_id': body.request_id})
            self.task = asyncio.create_task(self.run(authorized))
        except BaseException:
            self.collector.release_export('forward:' + body.request_id)
            self.job = self.store.get_setting(JOB, None)
            raise
        return self.status()

    async def control(self, job_id, action, authorized):
        if not self.job or self.job['id'] != job_id:
            raise ValueError('This request ID belongs to another action.')
        authorized()
        if action == 'pause':
            if self.job['state'] in {'running', 'waiting'}:
                self.job['state'] = 'pausing'
                self.save()
        elif action == 'cancel':
            if self.task and not self.task.done():
                self.job['state'] = 'cancelling'
                self.save()
            elif self.job['state'] not in TERMINAL:
                self.job['state'] = 'cancelled'
                self.save('cancelled')
        elif action == 'resume':
            if self.task and not self.task.done() or self.job['state'] in TERMINAL:
                return self.status()
            if self.job.get('creating') or self.job['state'] == 'creation_unknown':
                raise ValueError(UNCERTAIN_CREATE)
            interactions.permitted(self.collector)
            if self.account() != self.job['account_id']:
                raise ValueError('The Telegram account changed. Start a new transfer.')
            if not self.collector.reserve_export('forward:' + self.job['id']):
                raise ValueError(BUSY)
            owner = 'forward:' + self.job['id']
            try:
                self.job.update(state='running', error=None)
                self.save('resumed')
                self.task = asyncio.create_task(self.run(authorized))
            except BaseException:
                self.collector.release_export(owner)
                raise
        else:
            raise ValueError('Unknown action.')
        return self.status()

    def backoff(self, exc):
        until = time.time() + exc.seconds + 1
        with self.store.transaction():
            until = max(until, self.store.get_setting('rpc_backoff_until', 0) or 0)
            self.store.set_setting('rpc_backoff_until', until)
        return until

    def running(self):
        return self.job['state'] in {'running', 'waiting'}

    def settle(self):
        if self.job['state'] in {'pausing', 'cancelling', 'running', 'waiting'}:
            if self.job.get('creating'):
                self.job.update(state='creation_unknown', error=UNCERTAIN_CREATE)
            elif self.job.get('pending', {}).get('dispatched'):
                self.job.update(state='uncertain', error=UNCERTAIN_SEND)
            else:
                self.job['state'] = 'cancelled' if self.job['state'] == 'cancelling' else 'paused'

    async def wait(self, authorized, due=0):
        while self.running():
            authorized()
            interactions.check_restriction(self.store)
            if interactions.read_only(self.store):
                raise ValueError(interactions.READ_ONLY)
            until = max(due or 0, self.store.get_setting('rpc_backoff_until', 0) or 0)
            if until <= time.time():
                if self.job['state'] != 'running' or self.job['wait_until'] is not None:
                    self.job.update(state='running', wait_until=None)
                    self.save()
                return True
            if self.job.get('wait_until') != until:
                self.job.update(state='waiting', wait_until=until)
                self.save()
            await asyncio.sleep(min(1, until - time.time()))
        return False

    def skipped(self, ids, reason):
        self.job['cursor'] = ids[-1]
        self.job['skipped'] += len(ids)
        self.job['recent_skips'] = [*self.job['recent_skips'], {'ids': ids, 'reason': reason}][-20:]
        self.job['pending'] = {}
        self.save('skipped', {'ids': ids, 'reason': reason})

    async def page(self, source):
        messages = [message async for message in self.collector.client.iter_messages(source, limit=101,
            min_id=self.job['cursor'], max_id=self.job['upper_id'] + 1, reverse=True)]
        ids = [message.id for message in messages]
        if ids != sorted(set(ids)) or any(not self.job['cursor'] < number <= self.job['upper_id'] for number in ids):
            raise ValueError('The history page is not in message order.')
        if len(messages) > 100:
            group = getattr(messages[99], 'grouped_id', None)
            end = 100
            if group and group == getattr(messages[100], 'grouped_id', None):
                while end and getattr(messages[end-1], 'grouped_id', None) == group:
                    end -= 1
            if not end:
                raise ValueError('The album is too large to forward intact.')
            messages = messages[:end]
        return [list(group) for _, group in groupby(messages,
            key=lambda message: ('album', message.grouped_id) if getattr(message, 'grouped_id', None) else ('message', message.id))]

    async def run(self, authorized):
        job_id = self.job['id']
        source = destination = None
        units = []
        try:
            while await self.wait(authorized, (self.job.get('pending') or {}).get('due', self.job.get('create_due', 0))):
                operation = None
                try:
                    async with self.lock:
                        if not self.running():
                            break
                        authorized()
                        interactions.permitted(self.collector)
                        await asyncio.wait_for(self.collector.restore(), 60)
                        if self.account() != self.job['account_id']:
                            raise ValueError('The Telegram account changed. Start a new transfer.')
                        if source is None:
                            source = await asyncio.wait_for(self.source(self.job['source']), 60)
                        if self.job.get('destination') is None:
                            if not self.job.get('create_due'):
                                self.job['create_due'] = interactions.reserve(self.store, 'join')
                                self.save()
                                continue
                            if not self.running():
                                break
                            authorized()
                            interactions.permitted(self.collector)
                            operation = 'create'
                            self.job['creating'] = True
                            self.save('destination_requested', {'title': self.job['title'], 'mode': self.job['mode']})
                            response = await asyncio.wait_for(self.collector.client(functions.channels.CreateChannelRequest(
                                title=self.job['title'], about='', broadcast=self.job['mode'] == 'channel', megagroup=self.job['mode'] == 'group')), 60)
                            created = [chat for chat in response.chats if isinstance(chat, types.Channel) and chat.creator]
                            if len(created) != 1:
                                raise RuntimeError(UNCERTAIN_CREATE)
                            destination = created[0]
                            self.job.update(destination=utils.get_peer_id(destination), creating=False, create_due=0)
                            interactions.observe(self.collector, destination, add=False)
                            self.save('destination_created')
                        if destination is None:
                            destination = await asyncio.wait_for(self.destination(self.job['destination']), 60)
                        if not self.job['pending']:
                            if not units:
                                units = await asyncio.wait_for(self.page(source), 60)
                            if not self.running():
                                break
                            if not units:
                                self.job.update(state='completed', cursor=self.job['upper_id'])
                                self.save('completed')
                                break
                            unit = units.pop(0)
                            ids = [message.id for message in unit]
                            if any(not isinstance(message, types.Message) or getattr(message, 'action', None) for message in unit):
                                self.skipped(ids, 'service_message')
                                continue
                            if any(getattr(message, 'noforwards', False) for message in unit):
                                self.skipped(ids, 'forwarding_restricted')
                                continue
                            due = max(interactions.reserve(self.store, 'message') for _ in ids)
                            self.job['pending'] = {'ids': ids, 'random_ids': [secrets.randbits(63) or 1 for _ in ids], 'due': due, 'confirmed': {}, 'dispatched': False}
                            self.save()
                            continue
                        pending = self.job['pending']
                        if not self.running():
                            break
                        authorized()
                        interactions.permitted(self.collector)
                        operation = 'forward'
                        pending['dispatched'] = True
                        self.save()
                        response = await asyncio.wait_for(self.collector.client(functions.messages.ForwardMessagesRequest(
                            from_peer=source, id=pending['ids'], random_id=pending['random_ids'], to_peer=destination, silent=True)), 60)
                        confirmed = {str(update.random_id): update.id for update in getattr(response, 'updates', [])
                            if isinstance(update, types.UpdateMessageID) and update.random_id in pending['random_ids']}
                        added = set(confirmed) - set(pending['confirmed'])
                        pending['confirmed'].update(confirmed)
                        self.job['forwarded'] += len(added)
                        if len(pending['confirmed']) != len(pending['ids']):
                            self.job.update(state='uncertain', error=UNCERTAIN_SEND)
                            self.save('uncertain', {'source_ids': pending['ids'], 'confirmed': pending['confirmed']})
                            break
                        self.job['cursor'] = pending['ids'][-1]
                        details = {'source_ids': pending['ids'], 'destination_ids': [pending['confirmed'][str(number)] for number in pending['random_ids']]}
                        self.job['pending'] = {}
                        self.save('batch', details)
                except (*FLOOD_ERRORS, SlowModeWaitError) as exc:
                    self.backoff(exc)
                    if operation == 'create':
                        self.job['creating'] = False
                    if operation == 'forward':
                        self.job['pending']['dispatched'] = False
                    self.save('waiting', {'error_type': type(exc).__name__})
                except RPCError as exc:
                    interactions.note_restriction(self.store, exc)
                    if getattr(exc, 'code', 0) >= 500:
                        raise
                    if operation == 'create':
                        self.job['creating'] = False
                    pending = self.job['pending']
                    if operation == 'forward' and not pending['confirmed'] and type(exc).__name__ in ITEM_ERRORS:
                        self.skipped(pending['ids'], type(exc).__name__)
                        continue
                    if operation == 'forward':
                        pending['dispatched'] = False
                    uncertain = pending and pending['dispatched']
                    state = 'uncertain' if uncertain else 'cancelled' if self.job['state'] == 'cancelling' else 'paused'
                    self.job.update(state=state, error=UNCERTAIN_SEND if uncertain else type(exc).__name__)
                    self.save(state, {'error_type': type(exc).__name__})
                    break
        except (Exception, asyncio.CancelledError) as exc:
            self.job = self.store.get_setting(JOB, self.job)
            if self.job.get('creating'):
                self.job.update(state='creation_unknown', error=UNCERTAIN_CREATE)
            elif self.job.get('pending', {}).get('dispatched'):
                self.job.update(state='uncertain', error=UNCERTAIN_SEND)
            else:
                state = 'cancelled' if self.job['state'] == 'cancelling' else 'paused'
                self.job.update(state=state, error=str(exc) if isinstance(exc, ValueError) else type(exc).__name__)
            self.save(self.job['state'], {'error_type': type(exc).__name__})
        finally:
            try:
                if self.job['state'] in {'pausing', 'cancelling', 'running', 'waiting'}:
                    self.settle()
                    self.save(self.job['state'])
            finally:
                self.collector.release_export('forward:' + job_id)
                self.settle()

    async def close(self):
        if self.task and not self.task.done():
            job_id = self.job['id']
            try:
                self.task.cancel()
                await asyncio.gather(self.task, return_exceptions=True)
            finally:
                self.collector.release_export('forward:' + job_id)
                self.settle()
