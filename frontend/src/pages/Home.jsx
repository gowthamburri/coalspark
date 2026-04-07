/**
 * src/pages/Home.jsx
 * Landing page: Hero banner, restaurant stats, featured menu items,
 * cuisine categories, and a call-to-action.
 */
import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { Star, MapPin, Clock, Phone, ChevronRight, Flame } from 'lucide-react'
import { fetchMenuItems } from '../api/menuApi'
import { getRestaurant } from '../api/adminApi'
import FoodCard from '../components/FoodCard'
import { formatCurrency } from '../utils/formatCurrency'

const CUISINES = [
  { name: 'BBQ',             emoji: '🔥', desc: 'Slow-smoked to perfection'       },
  { name: 'Biryani & Mandi', emoji: '🍛', desc: 'Aromatic, layered, legendary'    },
  { name: 'Starters',        emoji: '🥙', desc: 'Bold flavours to kick things off' },
  { name: 'Main Course',     emoji: '🍽️', desc: 'Hearty mains from every corner'  },
  { name: 'Beverages',       emoji: '🥤', desc: 'Refresh and recharge'             },
  { name: 'Desserts',        emoji: '🍮', desc: 'Sweet endings done right'         },
]

export default function Home() {
  const [featured, setFeatured] = useState([])
  const [restaurant, setRestaurant] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const load = async () => {
      try {
        const [menuRes, restRes] = await Promise.all([
          fetchMenuItems({ is_featured: true }),
          getRestaurant(),
        ])
        setFeatured(menuRes.data.slice(0, 4))
        setRestaurant(restRes.data)
      } catch (err) {
        console.error('Failed to load home data', err)
      } finally {
        setLoading(false)
      }
    }
    load()
  }, [])

  return (
    <div className="min-h-screen">

      {/* ── HERO ──────────────────────────────────────────────────────── */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
        {/* Background */}
        <div
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: `url('https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=1600&q=80')`,
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-b from-coal-900/80 via-coal-900/70 to-coal-900" />
        {/* Ember glow */}
        <div className="absolute inset-0 bg-ember-glow" />

        {/* Hero content */}
        <div className="relative z-10 text-center px-4 max-w-4xl mx-auto animate-fade-in">
          <div className="flex items-center justify-center gap-2 mb-6">
            <div className="w-10 h-10 bg-ember-500 rounded-xl flex items-center justify-center shadow-ember">
              <Flame className="w-6 h-6 text-white" />
            </div>
            <span className="text-ember-500 font-semibold tracking-widest text-sm uppercase">
              CoalSpark Restaurant
            </span>
          </div>

          <h1 className="text-5xl sm:text-6xl md:text-7xl font-extrabold text-white leading-tight mb-4">
            Where Fire
            <span className="text-ember-500 block">Meets Flavour</span>
          </h1>

          <p className="text-gray-300 text-lg md:text-xl max-w-2xl mx-auto mb-8 leading-relaxed">
            Premium BBQ, Biryani, Mandi, Chinese & Italian — crafted with passion
            in the heart of Gachibowli, Hyderabad.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/menu" className="btn-primary text-base px-8 py-4">
              Explore Menu
            </Link>
            <a href="#about" className="btn-outline text-base px-8 py-4">
              Our Story
            </a>
          </div>

          {/* Quick stats */}
          {restaurant && (
            <div className="flex flex-wrap justify-center gap-6 mt-12">
              <div className="flex items-center gap-2 text-gray-300">
                <Star className="w-5 h-5 text-ember-500 fill-ember-500" />
                <span className="font-bold text-white">{restaurant.rating}</span>
                <span className="text-sm text-gray-400">({restaurant.total_reviews?.toLocaleString()} reviews)</span>
              </div>
              <div className="w-px h-5 bg-white/20 hidden sm:block" />
              <div className="flex items-center gap-2 text-gray-300">
                <Clock className="w-4 h-4 text-ember-500" />
                <span className="text-sm">{restaurant.opening_time} – {restaurant.closing_time}</span>
              </div>
              <div className="w-px h-5 bg-white/20 hidden sm:block" />
              <div className="flex items-center gap-2 text-gray-300">
                <MapPin className="w-4 h-4 text-ember-500" />
                <span className="text-sm">Gachibowli, Hyderabad</span>
              </div>
            </div>
          )}
        </div>

        {/* Scroll indicator */}
        <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
          <div className="w-6 h-10 border-2 border-white/20 rounded-full flex justify-center pt-2">
            <div className="w-1 h-3 bg-ember-500 rounded-full" />
          </div>
        </div>
      </section>

      {/* ── CUISINE CATEGORIES ────────────────────────────────────────── */}
      <section className="py-20 px-4 max-w-7xl mx-auto" id="about">
        <div className="text-center mb-12">
          <h2 className="section-title">Explore Our Cuisines</h2>
          <p className="section-subtitle">Six distinct flavour worlds under one roof</p>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
          {CUISINES.map(({ name, emoji, desc }) => (
            <Link
              key={name}
              to={`/menu?category=${encodeURIComponent(name)}`}
              className="card p-5 text-center hover:border-ember-500/30 hover:-translate-y-1
                         transition-all duration-300 group"
            >
              <span className="text-3xl block mb-3">{emoji}</span>
              <h3 className="text-white font-semibold text-sm mb-1">{name}</h3>
              <p className="text-gray-500 text-xs leading-relaxed">{desc}</p>
            </Link>
          ))}
        </div>
      </section>

      {/* ── FEATURED ITEMS ────────────────────────────────────────────── */}
      <section className="py-20 px-4 max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-10">
          <div>
            <h2 className="section-title">Chef's Picks</h2>
            <p className="section-subtitle">Our most-loved, hand-picked specials</p>
          </div>
          <Link to="/menu" className="flex items-center gap-1 text-ember-500 hover:text-ember-400
                                       text-sm font-medium transition-colors">
            View All <ChevronRight className="w-4 h-4" />
          </Link>
        </div>

        {loading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="skeleton h-80 rounded-2xl" />
            ))}
          </div>
        ) : featured.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {featured.map((item) => <FoodCard key={item.id} item={item} />)}
          </div>
        ) : (
          <div className="text-center py-16 text-gray-500">
            <p>No featured items yet. Check back soon!</p>
          </div>
        )}
      </section>

      {/* ── ABOUT / INFO STRIP ─────────────────────────────────────────── */}
      {restaurant && (
        <section className="bg-ash-100 border-y border-white/5 py-16 px-4">
          <div className="max-w-5xl mx-auto grid md:grid-cols-3 gap-8 text-center">
            <div>
              <MapPin className="w-8 h-8 text-ember-500 mx-auto mb-3" />
              <h4 className="text-white font-semibold mb-1">Find Us</h4>
              <p className="text-gray-400 text-sm">{restaurant.address}</p>
              <p className="text-gray-400 text-sm">{restaurant.city}</p>
            </div>
            <div>
              <Clock className="w-8 h-8 text-ember-500 mx-auto mb-3" />
              <h4 className="text-white font-semibold mb-1">Opening Hours</h4>
              <p className="text-gray-400 text-sm">Every day</p>
              <p className="text-gray-400 text-sm">{restaurant.opening_time} – {restaurant.closing_time}</p>
            </div>
            <div>
              <Phone className="w-8 h-8 text-ember-500 mx-auto mb-3" />
              <h4 className="text-white font-semibold mb-1">Reservations</h4>
              <p className="text-gray-400 text-sm">{restaurant.phone}</p>
              <p className="text-gray-400 text-sm">{restaurant.email}</p>
            </div>
          </div>
        </section>
      )}

      {/* ── CTA ───────────────────────────────────────────────────────── */}
      <section className="py-24 px-4 text-center">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-4xl font-extrabold text-white mb-4">
            Ready to ignite your taste buds?
          </h2>
          <p className="text-gray-400 mb-8">
            Order online and experience CoalSpark's signature flavours delivered to your door.
          </p>
          <Link to="/menu" className="btn-primary text-base px-10 py-4">
            Order Now
          </Link>
        </div>
      </section>
    </div>
  )
}