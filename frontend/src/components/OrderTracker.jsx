import { Clock, ChefHat, PackageCheck } from 'lucide-react'

const steps = [
  { key: 'pending', label: 'Pending', icon: Clock },
  { key: 'preparing', label: 'Preparing', icon: ChefHat },
  { key: 'delivered', label: 'Delivered', icon: PackageCheck },
]

const statusRank = { pending: 0, confirmed: 0, preparing: 1, ready: 1, delivered: 2, cancelled: -1 }

export default function OrderTracker({ status }) {
  const rank = statusRank[status] ?? 0
  const isCancelled = status === 'cancelled'

  return (
    <div className="mt-3">
      {isCancelled ? (
        <p className="text-xs text-red-400">Order cancelled</p>
      ) : (
        <div className="flex items-center gap-2">
          {steps.map((step, i) => {
            const Icon = step.icon
            const active = i <= rank
            return (
              <div key={step.key} className="flex items-center gap-2">
                <div className={`w-7 h-7 rounded-full flex items-center justify-center border ${active ? 'bg-ember-500/20 border-ember-500 text-ember-500' : 'bg-ash-200 border-white/10 text-gray-500'}`}>
                  <Icon className="w-3.5 h-3.5" />
                </div>
                <span className={`text-[11px] ${active ? 'text-gray-200' : 'text-gray-500'}`}>{step.label}</span>
                {i < steps.length - 1 && <div className={`w-6 h-px ${i < rank ? 'bg-ember-500' : 'bg-white/10'}`} />}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

