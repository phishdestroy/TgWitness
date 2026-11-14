export function createSaveQueue(delay = 400) {
  let pending = null, timer = null, running = false, closed = null;
  function schedule() {
    clearTimeout(timer);
    if (pending && !running) timer = setTimeout(flush, Math.max(0, pending.due - performance.now()));
  }
  async function flush() {
    if (!pending || running) return;
    const batch = pending; pending = null; running = true;
    try {
      const result = await batch.write();
      for (const waiter of batch.waiters) waiter.resolve(result);
    } catch (error) {
      for (const waiter of batch.waiters) waiter.reject(error);
    } finally {running = false; schedule();}
  }
  return {
    save(write) {
      if (closed) return Promise.reject(closed);
      if (!pending) pending = {waiters: []};
      pending.write = write; pending.due = performance.now() + delay;
      const promise = new Promise((resolve, reject) => pending.waiters.push({resolve, reject}));
      schedule(); return promise;
    },
    close(error) {
      closed = error; clearTimeout(timer);
      if (pending) for (const waiter of pending.waiters) waiter.reject(error);
      pending = null;
    },
  };
}
