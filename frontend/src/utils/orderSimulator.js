/*
  Lightweight order simulator for demoing status progression locally.
  Stores simulation metadata in localStorage under 'simOrders'.
  When creating an order, schedule timed updates (if app stays open), and
  persist current status so Orders page can reflect it across reloads.
*/

const KEY = 'simOrders'

const DEFAULT_STEPS = ['pending', 'preparing', 'ready', 'delivered']

function read() {
  try {
    return JSON.parse(localStorage.getItem(KEY) || '[]')
  } catch (e) {
    return []
  }
}

function write(list) {
  localStorage.setItem(KEY, JSON.stringify(list))
}

export function createSimulatedOrder(orderData = {}, opts = {}) {
  const list = read()

  const entry = {
    id: orderData.id || Date.now(),
    statusIndex: 0,
    steps: DEFAULT_STEPS,
    created_at: orderData.created_at || new Date().toISOString(),
    paid: !!opts.paid || orderData.paid || false,
    payment_method: orderData.payment_method || opts.payment_method || 'cod',
    total_amount: orderData.total_amount || orderData.total || 0,
    items: orderData.items || opts.items || [],
    raw: orderData,
  }

  list.push(entry)
  write(list)

  // Schedule updates while app is open — times configurable (in ms)
  const intervals = [5000, 10000, 15000] // after 5s, 10s, 15s
  intervals.forEach((delay) => {
    setTimeout(() => {
      advanceStatus(entry.id)
    }, delay)
  })

  return entry
}

export function getSimulatedOrder(id) {
  const list = read()
  return list.find((i) => i.id === id)
}

export function getAllSimulatedOrders() {
  return read()
}

export function advanceStatus(id) {
  const list = read()
  const i = list.findIndex((l) => l.id === id)
  if (i === -1) return
  const entry = list[i]
  if (entry.statusIndex < entry.steps.length - 1) {
    entry.statusIndex += 1
    list[i] = entry
    write(list)
  }
}

export function clearSimulatedOrders() {
  localStorage.removeItem(KEY)
}
