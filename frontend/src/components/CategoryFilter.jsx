/**
 * src/components/CategoryFilter.jsx
 * Horizontal scrollable category pill filters for the menu page.
 */
import { Flame, Utensils, Coffee, IceCream, ChefHat, Soup } from 'lucide-react'

const CATEGORIES = [
  { label: 'All',             value: '',                icon: ChefHat   },
  { label: 'BBQ',             value: 'BBQ',             icon: Flame      },
  { label: 'Biryani & Mandi', value: 'Biryani & Mandi', icon: Soup       },
  { label: 'Starters',        value: 'Starters',        icon: Utensils   },
  { label: 'Main Course',     value: 'Main Course',     icon: Utensils   },
  { label: 'Beverages',       value: 'Beverages',       icon: Coffee     },
  { label: 'Desserts',        value: 'Desserts',        icon: IceCream   },
]

export default function CategoryFilter({ active, onChange }) {
  return (
    <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-hide">
      {CATEGORIES.map(({ label, value, icon: Icon }) => {
        const isActive = active === value
        return (
          <button
            key={value}
            onClick={() => onChange(value)}
            className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-medium
                        whitespace-nowrap transition-all duration-200 flex-shrink-0
                        ${isActive
                          ? 'bg-ember-500 text-white shadow-ember'
                          : 'bg-ash-100 text-gray-400 hover:text-white hover:bg-ash-200 border border-white/5'
                        }`}
          >
            <Icon className="w-3.5 h-3.5" />
            {label}
          </button>
        )
      })}
    </div>
  )
}