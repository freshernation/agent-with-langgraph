# Week 2 — State

> **Destination**
> Helpdesk, a support agent for an online shop, takes a customer's ticket, sorts it
> into a form, looks up the order with tools that can only see that customer's
> orders, and drafts a reply — and you can defend every key in its state.

A new agent. Desk was yours; Helpdesk is the kind of agent people are paid to build.

---

## The week

| Day | Folder | What you'll be able to do |
|---|---|---|
| Mon | `day-1/` | Say what happens when two nodes write the same key, and choose a reducer |
| Tue | `day-2/` | Make a model fill in a typed form, and cope when it will not |
| Wed | `day-3/` | Give tools the state the model must not control — whose orders they read |
| Thu | `day-4/` | Route a ticket through classify, look up and draft, with retries and a backup model |
| Fri | `milestone/` | Helpdesk, measured on twenty labelled tickets, and its shape defended |

---

## The rule from this week on

**Every key in the state is read by some node.** If nothing reads it, delete it. If a
node needs something the state does not hold, the state is wrong, not the node.

---

## Meet the shop

`shop/` is given: five customers, ten orders, twenty tickets a person labelled, and a
refund function that writes to a throwaway file. Read `shop/__init__.py` on Monday.

---

## Outside-view question

> *An air-traffic controller keeps one paper strip per flight. What is on it, and what
> is deliberately not?*
