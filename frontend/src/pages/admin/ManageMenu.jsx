/**
 * src/pages/admin/ManageMenu.jsx
 * Admin menu management — list, create, edit, delete items, upload images.
 */
import { useEffect, useState } from 'react'
import { Plus, Pencil, Trash2, Upload, X, Check } from 'lucide-react'
import toast from 'react-hot-toast'
import {
  fetchMenuItems, createMenuItem, updateMenuItem,
  deleteMenuItem, uploadMenuImage,
} from '../../api/menuApi'
import { formatCurrency } from '../../utils/formatCurrency'

const CATEGORIES = ['BBQ','Biryani & Mandi','Starters','Main Course','Beverages','Desserts']
const EMPTY_FORM = {
  name:'', description:'', price:'', category:'BBQ',
  is_vegetarian: false, is_available: true, is_featured: false,
  spice_level: 2, preparation_time: 20, restaurant_id: 1,
}

export default function ManageMenu() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [uploadingId, setUploadingId] = useState(null)

  const load = async () => {
    try {
      const res = await fetchMenuItems({ is_available: undefined })
      setItems(res.data)
    } catch { toast.error('Failed to load menu') }
    finally { setLoading(false) }
  }

  useEffect(() => { load() }, [])

  const openCreate = () => { setEditing(null); setForm(EMPTY_FORM); setShowForm(true) }
  const openEdit   = (item) => {
    setEditing(item)
    setForm({ ...item, price: item.price.toString() })
    setShowForm(true)
  }
  const closeForm = () => { setShowForm(false); setEditing(null); setForm(EMPTY_FORM) }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setForm((f) => ({ ...f, [name]: type === 'checkbox' ? checked : value }))
  }

  const handleSave = async (e) => {
    e.preventDefault()
    setSaving(true)
    try {
      const payload = { ...form, price: parseFloat(form.price) }
      if (editing) {
        await updateMenuItem(editing.id, payload)
        toast.success('Item updated!')
      } else {
        await createMenuItem(payload)
        toast.success('Item created!')
      }
      closeForm()
      load()
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Save failed')
    } finally { setSaving(false) }
  }

  const handleDelete = async (id, name) => {
    if (!confirm(`Delete "${name}"?`)) return
    try {
      await deleteMenuItem(id)
      toast.success('Item deleted')
      load()
    } catch { toast.error('Delete failed') }
  }

  const handleImageUpload = async (id, file) => {
    setUploadingId(id)
    try {
      const fd = new FormData()
      fd.append('file', file)
      await uploadMenuImage(id, fd)
      toast.success('Image uploaded!')
      load()
    } catch { toast.error('Image upload failed') }
    finally { setUploadingId(null) }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Manage Menu</h1>
          <p className="text-gray-500 text-sm mt-1">{items.length} items total</p>
        </div>
        <button onClick={openCreate} className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" /> Add Item
        </button>
      </div>

      {/* ── Form modal ──────────────────────────────────────────────── */}
      {showForm && (
        <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4">
          <div className="bg-coal-900 border border-white/10 rounded-2xl w-full max-w-2xl
                          max-h-[90vh] overflow-y-auto p-6 animate-slide-up">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-white font-bold text-xl">
                {editing ? 'Edit Item' : 'New Menu Item'}
              </h2>
              <button onClick={closeForm} className="text-gray-500 hover:text-white transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSave} className="space-y-4">
              <div className="grid sm:grid-cols-2 gap-4">
                <div className="sm:col-span-2">
                  <label className="text-gray-400 text-sm mb-1 block">Item Name *</label>
                  <input name="name" value={form.name} onChange={handleChange}
                         required placeholder="e.g. Smoked BBQ Ribs"
                         className="input-field" />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Price (₹) *</label>
                  <input name="price" type="number" step="0.01" min="1"
                         value={form.price} onChange={handleChange}
                         required placeholder="299"
                         className="input-field" />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Category *</label>
                  <select name="category" value={form.category} onChange={handleChange}
                          className="input-field">
                    {CATEGORIES.map((c) => <option key={c}>{c}</option>)}
                  </select>
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Spice Level (1–5)</label>
                  <input name="spice_level" type="number" min="1" max="5"
                         value={form.spice_level} onChange={handleChange}
                         className="input-field" />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Prep Time (min)</label>
                  <input name="preparation_time" type="number" min="1"
                         value={form.preparation_time} onChange={handleChange}
                         className="input-field" />
                </div>
                <div className="sm:col-span-2">
                  <label className="text-gray-400 text-sm mb-1 block">Description</label>
                  <textarea name="description" rows={3} value={form.description}
                            onChange={handleChange}
                            placeholder="Describe this dish…"
                            className="input-field resize-none" />
                </div>
              </div>

              {/* Toggles */}
              <div className="flex flex-wrap gap-6 pt-2">
                {[
                  { name: 'is_vegetarian', label: 'Vegetarian' },
                  { name: 'is_available',  label: 'Available'  },
                  { name: 'is_featured',   label: "Chef's Pick" },
                ].map(({ name, label }) => (
                  <label key={name} className="flex items-center gap-2 cursor-pointer select-none">
                    <div className={`w-10 h-5 rounded-full transition-colors relative
                                    ${form[name] ? 'bg-ember-500' : 'bg-ash-100'}`}>
                      <div className={`w-4 h-4 bg-white rounded-full absolute top-0.5
                                      transition-transform ${form[name] ? 'translate-x-5' : 'translate-x-0.5'}`} />
                    </div>
                    <input type="checkbox" name={name} checked={form[name]}
                           onChange={handleChange} className="sr-only" />
                    <span className="text-gray-300 text-sm">{label}</span>
                  </label>
                ))}
              </div>

              <div className="flex gap-3 pt-2">
                <button type="button" onClick={closeForm} className="btn-ghost flex-1">Cancel</button>
                <button type="submit" disabled={saving} className="btn-primary flex-1 flex items-center justify-center gap-2">
                  {saving ? <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                           : <><Check className="w-4 h-4" /> {editing ? 'Save Changes' : 'Create Item'}</>}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* ── Items table ──────────────────────────────────────────────── */}
      {loading ? (
        <div className="space-y-3">
          {Array.from({ length: 5 }).map((_, i) => <div key={i} className="skeleton h-16 rounded-xl" />)}
        </div>
      ) : (
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="border-b border-white/5">
                <tr className="text-gray-500 text-left">
                  <th className="px-5 py-3 font-medium">Item</th>
                  <th className="px-5 py-3 font-medium">Category</th>
                  <th className="px-5 py-3 font-medium">Price</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium">Image</th>
                  <th className="px-5 py-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {items.map((item) => (
                  <tr key={item.id} className="border-b border-white/5 hover:bg-white/2 transition-colors">
                    <td className="px-5 py-4">
                      <p className="text-white font-medium">{item.name}</p>
                      <p className="text-gray-600 text-xs mt-0.5 max-w-[200px] truncate">{item.description}</p>
                    </td>
                    <td className="px-5 py-4 text-gray-400">{item.category}</td>
                    <td className="px-5 py-4 text-ember-500 font-semibold">{formatCurrency(item.price)}</td>
                    <td className="px-5 py-4">
                      <span className={`badge ${item.is_available ? 'bg-green-400/10 text-green-400' : 'bg-red-400/10 text-red-400'}`}>
                        {item.is_available ? 'Available' : 'Unavailable'}
                      </span>
                    </td>
                    <td className="px-5 py-4">
                      <label className="cursor-pointer flex items-center gap-1.5 text-gray-400 hover:text-white transition-colors">
                        {uploadingId === item.id
                          ? <div className="w-4 h-4 border-2 border-ember-500 border-t-transparent rounded-full animate-spin" />
                          : <Upload className="w-4 h-4" />
                        }
                        <span className="text-xs">{item.image_url ? 'Change' : 'Upload'}</span>
                        <input
                          type="file" accept="image/*" className="sr-only"
                          onChange={(e) => e.target.files[0] && handleImageUpload(item.id, e.target.files[0])}
                        />
                      </label>
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button onClick={() => openEdit(item)}
                                className="p-2 rounded-lg bg-ash-100 hover:bg-ash-200 text-gray-400
                                           hover:text-white transition-colors">
                          <Pencil className="w-3.5 h-3.5" />
                        </button>
                        <button onClick={() => handleDelete(item.id, item.name)}
                                className="p-2 rounded-lg bg-red-500/10 hover:bg-red-500/20
                                           text-red-400 transition-colors">
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {items.length === 0 && (
              <div className="text-center py-16 text-gray-500">
                No menu items yet. Click "Add Item" to get started.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}