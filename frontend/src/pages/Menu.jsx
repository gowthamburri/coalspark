
import { useEffect, useState, useCallback } from 'react'
import { useSearchParams } from 'react-router-dom'
import { Search, SlidersHorizontal, X } from 'lucide-react'
import { fetchMenuItems } from '../api/menuApi'
import FoodCard from '../components/FoodCard'
import CategoryFilter from '../components/CategoryFilter'

export default function Menu() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [category, setCategory] = useState(searchParams.get('category') || '')
  const [debouncedSearch, setDebouncedSearch] = useState('')

  // Debounce search input (300ms)
  useEffect(() => {
    const t = setTimeout(() => setDebouncedSearch(search), 300)
    return () => clearTimeout(t)
  }, [search])

  // Fetch menu items when filters change
  const loadItems = useCallback(async () => {
    setLoading(true)
    try {
      const params = {}
      if (category) params.category = category
      if (debouncedSearch) params.search = debouncedSearch
      const res = await fetchMenuItems(params)
      setItems(res.data)
    } catch (err) {
      console.error('Failed to load menu', err)
    } finally {
      setLoading(false)
    }
  }, [category, debouncedSearch])

  useEffect(() => { loadItems() }, [loadItems])

  const handleCategoryChange = (cat) => {
    setCategory(cat)
    setSearchParams(cat ? { category: cat } : {})
  }

  const clearSearch = () => setSearch('')

  return (
    <div className="min-h-screen pt-20 pb-16 px-4">
      <div className="max-w-7xl mx-auto">

        {/* ── Page header ─────────────────────────────────────────────── */}
        <div className="text-center mb-10 pt-8 animate-fade-in">
          <h1 className="section-title text-4xl">Our Menu</h1>
          <p className="section-subtitle mt-2">
            Explore {items.length > 0 ? items.length + ' dishes across' : 'dishes across'}  6 flavour-packed categories
          </p>
        </div>

        {/* ── Search bar ──────────────────────────────────────────────── */}
        <div className="relative max-w-xl mx-auto mb-8">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-500" />
          <input
            type="text"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search dishes, ingredients…"
            className="input-field pl-12 pr-12"
          />
          {search && (
            <button
              onClick={clearSearch}
              className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-500
                         hover:text-white transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* ── Category filter ──────────────────────────────────────────── */}
        <div className="mb-8">
          <CategoryFilter active={category} onChange={handleCategoryChange} />
        </div>

        {/* ── Results info ─────────────────────────────────────────────── */}
        {!loading && (
          <div className="flex items-center justify-between mb-6">
            <p className="text-gray-500 text-sm">
              {items.length === 0
                ? 'No items found'
                : `Showing ${items.length} item${items.length !== 1 ? 's' : ''}`
              }
              {category && <span className="text-ember-500"> in {category}</span>}
              {debouncedSearch && <span className="text-ember-500"> for "{debouncedSearch}"</span>}
            </p>
            {(category || debouncedSearch) && (
              <button
                onClick={() => { setCategory(''); clearSearch(); setSearchParams({}) }}
                className="text-sm text-ember-500 hover:text-ember-400 flex items-center gap-1"
              >
                <X className="w-3.5 h-3.5" /> Clear filters
              </button>
            )}
          </div>
        )}

        {/* ── Menu grid ────────────────────────────────────────────────── */}
        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {Array.from({ length: 8 }).map((_, i) => (
              <div key={i} className="skeleton h-80 rounded-2xl" />
            ))}
          </div>
        ) : items.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-24 gap-4 text-center">
            <span className="text-6xl">🔍</span>
            <h3 className="text-white font-semibold text-xl">No items found</h3>
            <p className="text-gray-500 text-sm max-w-xs">
              Try a different category or search term. Our full menu has something for everyone!
            </p>
            <button
              onClick={() => { setCategory(''); clearSearch(); setSearchParams({}) }}
              className="btn-outline text-sm py-2 px-6 mt-2"
            >
              View all items
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {items.map((item) => <FoodCard key={item.id} item={item} />)}
          </div>
        )}
      </div>
    </div>
  )
}