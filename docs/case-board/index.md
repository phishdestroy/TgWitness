# Build a Case Board

Canonical page: https://phishdestroy.github.io/TgWitness/docs/case-board/

Turn saved Telegram observations into a case your team can review together.

Case Board keeps bookmarks, exact-text highlights, saved slices and discussion beside their source references. A collection gives the case a working structure; signed revisions preserve how the team developed it.

## From a message to a case card

1. Open **Investigation → Case Board** in Standard or Expert mode. Create a collection for the case and choose its chat scope.
2. In **Journal** or a saved chat, choose **To board**, or focus the record and press **B**. The card enters Inbox; give it a useful title and move it to your collection.
3. Select a passage in a saved chat message and choose **Highlight → board** to retain the exact quote and message version. Add a note explaining why it matters.
4. Discuss the card, assign a review status, and return to its source context whenever a claim needs checking. Use **Presentation** to walk through the collection with colleagues.

### Follow one changed payment link

Synthetic example · local illustration

1. **Capture.** Open saved observation #142 and its message version.
2. **Bookmark.** Keep the quote, source reference and your question on a card.
3. **Review.** Add a team comment and move the card to Review.
4. **Present.** Walk through the collection and open the cited source context.

#### Saved observation #142

“Use the new payment link.”

Operations chat · message 38 · observed 09:12 UTC

#### Card: changed destination

> Use the new payment link.

Question: which destination appeared in the earlier version?

#### Team review

Analyst: compare with observation #101.

Status: Review · revision retained

#### Source context

Card → saved version → earlier observation

The annotation and the Telegram observation remain separately identifiable.

## Save a useful range once

Shift-click two records in one chat for **Slice between**, choose **Slice by time**, or save the current Journal filters. Review the count before saving. Reopen the slice to apply its saved query; **Show records added since bookmark** reveals later additions.

A time slice follows collector observation time. A message-ID slice can follow the selected messages as later changes arrive. The saved creation boundary lets a recipient compare the original selection with its later state.

## Give each colleague the right role

**Reviewer** reads the board; **Analyst** adds cards and comments; **Operator** also manages collections and review decisions. Workspace and chat permissions apply to cards, source context and discussions. Use named access grants for clear attribution.

## Carry the work into a deliverable

Export a slice as signed JSON, or use CSV for a spreadsheet. Report settings can include bookmarks and slices, with team comments when selected. Choose these contents in [Report studio](https://phishdestroy.github.io/TgWitness/docs/reports/); a saved slice does not automatically configure a report. For a restricted recipient, use the separate [handover controls](https://phishdestroy.github.io/TgWitness/docs/handover/).

Read the [Case Board reference](https://phishdestroy.github.io/TgWitness/docs/reference/case-board/) for signed revisions, exact quote matching, selection verification and permissions.
