import { useEffect, useMemo, useState } from 'react'
import toast from 'react-hot-toast'
import { Plus, Pencil, Trash2, X, Check, TicketPercent } from 'lucide-react'

import { createCoupon, deleteCoupon, getCoupons, updateCoupon } from '../../api/couponApi'
import { getErrorMessage } from '../../utils/error'

const EMPTY_FORM = {
  restaurant_id: 1,
  code: '',
  discount_type: 'percentage',
  discount_value: 10,
  min_order_amount: 0,
  max_discount_amount: '',
  usage_limit: '',
  starts_at: '',
  expires_at: '',
  is_active: true,
}

function toInputDatetimeLocal(d) {
  if (!d) return ''
  const dt = new Date(d)
  const pad = (n) => String(n).padStart(2, '0')
  return `${dt.getFullYear()}-${pad(dt.getMonth() + 1)}-${pad(dt.getDate())}T${pad(dt.getHours())}:${pad(dt.getMinutes())}`
}

export default function ManageCoupons() {
  const [coupons, setCoupons] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [editing, setEditing] = useState(null)
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)

  const load = async () => {
    setLoading(true)
    try {
      const res = await getCoupons()
      setCoupons(res.data)
    } catch {
      toast.error('Failed to load coupons')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load() }, [])

  const openCreate = () => {
    setEditing(null)
    const now = new Date()
    const in30 = new Date(Date.now() + 1000 * 60 * 60 * 24 * 30)
    setForm({
      ...EMPTY_FORM,
      starts_at: toInputDatetimeLocal(now),
      expires_at: toInputDatetimeLocal(in30),
    })
    setShowForm(true)
  }

  const openEdit = (coupon) => {
    setEditing(coupon)
    setForm({
      restaurant_id: coupon.restaurant_id,
      code: coupon.code,
      discount_type: coupon.discount_type,
      discount_value: coupon.discount_value,
      min_order_amount: coupon.min_order_amount,
      max_discount_amount: coupon.max_discount_amount ?? '',
      usage_limit: coupon.usage_limit ?? '',
      starts_at: toInputDatetimeLocal(coupon.starts_at),
      expires_at: toInputDatetimeLocal(coupon.expires_at),
      is_active: coupon.is_active,
    })
    setShowForm(true)
  }

  const closeForm = () => {
    setShowForm(false)
    setEditing(null)
    setForm(EMPTY_FORM)
  }

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target
    setForm((f) => ({ ...f, [name]: type === 'checkbox' ? checked : value }))
  }

  const payloadFromForm = useMemo(() => {
    const base = {
      restaurant_id: Number(form.restaurant_id),
      code: form.code,
      discount_type: form.discount_type,
      discount_value: Number(form.discount_value),
      min_order_amount: Number(form.min_order_amount || 0),
      is_active: !!form.is_active,
      starts_at: new Date(form.starts_at).toISOString(),
      expires_at: new Date(form.expires_at).toISOString(),
    }
    const opt = {}
    if (form.max_discount_amount !== '') opt.max_discount_amount = Number(form.max_discount_amount)
    if (form.usage_limit !== '') opt.usage_limit = Number(form.usage_limit)
    return { ...base, ...opt }
  }, [form])

  const handleSave = async (e) => {
    e.preventDefault()
    if (!form.code.trim()) {
      toast.error('Coupon code is required')
      return
    }
    if (!form.starts_at || !form.expires_at) {
      toast.error('Start and expiry are required')
      return
    }
    // Basic client-side numeric validation
    const discountValue = Number(form.discount_value)
    if (!Number.isFinite(discountValue) || discountValue <= 0) {
      toast.error('Discount value must be a positive number')
      return
    }
    if (form.discount_type === 'percentage' && discountValue > 100) {
      toast.error('Percentage discount cannot exceed 100%')
      return
    }
    const minOrder = Number(form.min_order_amount || 0)
    if (!Number.isFinite(minOrder) || minOrder < 0) {
      toast.error('Min order amount must be 0 or greater')
      return
    }
    if (form.max_discount_amount !== '') {
      const maxDisc = Number(form.max_discount_amount)
      if (!Number.isFinite(maxDisc) || maxDisc < 0) {
        toast.error('Max discount must be 0 or greater')
        return
      }
    }
    if (form.usage_limit !== '') {
      const usage = Number(form.usage_limit)
      if (!Number.isFinite(usage) || usage < 0) {
        toast.error('Usage limit must be 0 or greater')
        return
      }
    }
    setSaving(true)
    try {
      if (editing) {
        await updateCoupon(editing.id, payloadFromForm)
        toast.success('Coupon updated')
      } else {
        await createCoupon(payloadFromForm)
        toast.success('Coupon created')
      }
      closeForm()
      load()
    } catch (err) {
      const msg = getErrorMessage(err)
      toast.error(msg || 'Save failed')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (coupon) => {
    if (!confirm(`Delete coupon "${coupon.code}"?`)) return
    try {
      await deleteCoupon(coupon.id)
      toast.success('Coupon deleted')
      load()
    } catch {
      toast.error('Delete failed')
    }
  }

  const toggleActive = async (coupon) => {
    try {
      await updateCoupon(coupon.id, { is_active: !coupon.is_active })
      setCoupons((prev) => prev.map((c) => (c.id === coupon.id ? { ...c, is_active: !c.is_active } : c)))
      toast.success(`${coupon.code} ${coupon.is_active ? 'deactivated' : 'activated'}`)
    } catch {
      toast.error('Update failed')
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Manage Coupons</h1>
          <p className="text-gray-500 text-sm mt-1">{coupons.length} coupons total</p>
        </div>
        <button onClick={openCreate} className="btn-primary flex items-center gap-2">
          <Plus className="w-4 h-4" /> New Coupon
        </button>
      </div>

      {showForm && (
        <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center p-4">
          <div className="bg-coal-900 border border-white/10 rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-y-auto p-6 animate-slide-up">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-white font-bold text-xl">{editing ? 'Edit Coupon' : 'New Coupon'}</h2>
              <button onClick={closeForm} className="text-gray-500 hover:text-white transition-colors">
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSave} className="space-y-4">
              <div className="grid sm:grid-cols-2 gap-4">
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Code *</label>
                  <input name="code" value={form.code} onChange={handleChange} className="input-field" placeholder="BBQ20" />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Type *</label>
                  <select name="discount_type" value={form.discount_type} onChange={handleChange} className="input-field">
                    <option value="percentage">Percentage</option>
                    <option value="fixed">Fixed</option>
                  </select>
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">
                    Value * {form.discount_type === 'percentage' ? '(%)' : '(₹)'}
                  </label>
                  <input name="discount_value" type="number" min="1" step="0.01" value={form.discount_value} onChange={handleChange} className="input-field" />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Min Order (₹)</label>
                  <input name="min_order_amount" type="number" min="0" step="0.01" value={form.min_order_amount} onChange={handleChange} className="input-field" />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Max Discount (₹)</label>
                  <input name="max_discount_amount" type="number" min="0" step="0.01" value={form.max_discount_amount} onChange={handleChange} className="input-field" placeholder="optional" />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Usage Limit</label>
                  <input name="usage_limit" type="number" min="0" step="1" value={form.usage_limit} onChange={handleChange} className="input-field" placeholder="optional" />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Starts At *</label>
                  <input name="starts_at" type="datetime-local" value={form.starts_at} onChange={handleChange} className="input-field" />
                </div>
                <div>
                  <label className="text-gray-400 text-sm mb-1 block">Expires At *</label>
                  <input name="expires_at" type="datetime-local" value={form.expires_at} onChange={handleChange} className="input-field" />
                </div>
              </div>

              <label className="flex items-center gap-2 cursor-pointer select-none">
                <input type="checkbox" name="is_active" checked={form.is_active} onChange={handleChange} />
                <span className="text-gray-300 text-sm">Active</span>
              </label>

              <div className="flex gap-3 pt-2">
                <button type="button" onClick={closeForm} className="btn-ghost flex-1">Cancel</button>
                <button type="submit" disabled={saving} className="btn-primary flex-1 flex items-center justify-center gap-2">
                  {saving ? (
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  ) : (
                    <>
                      <Check className="w-4 h-4" /> {editing ? 'Save Changes' : 'Create Coupon'}
                    </>
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

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
                  <th className="px-5 py-3 font-medium">Code</th>
                  <th className="px-5 py-3 font-medium">Type</th>
                  <th className="px-5 py-3 font-medium">Value</th>
                  <th className="px-5 py-3 font-medium">Min Order</th>
                  <th className="px-5 py-3 font-medium">Uses</th>
                  <th className="px-5 py-3 font-medium">Status</th>
                  <th className="px-5 py-3 font-medium text-right">Actions</th>
                </tr>
              </thead>
              <tbody>
                {coupons.map((c) => (
                  <tr key={c.id} className="border-b border-white/5 hover:bg-white/2 transition-colors">
                    <td className="px-5 py-4">
                      <div className="flex items-center gap-2">
                        <div className="w-8 h-8 bg-ember-500/10 rounded-lg flex items-center justify-center">
                          <TicketPercent className="w-4 h-4 text-ember-500" />
                        </div>
                        <div>
                          <p className="text-white font-semibold tracking-wide">{c.code}</p>
                          <p className="text-gray-600 text-xs">#{c.id}</p>
                        </div>
                      </div>
                    </td>
                    <td className="px-5 py-4 text-gray-400 capitalize">{c.discount_type}</td>
                    <td className="px-5 py-4 text-ember-500 font-semibold">
                      {c.discount_type === 'percentage' ? `${c.discount_value}%` : `₹${c.discount_value}`}
                    </td>
                    <td className="px-5 py-4 text-gray-400">₹{c.min_order_amount}</td>
                    <td className="px-5 py-4 text-gray-400">{c.used_count}{c.usage_limit != null ? ` / ${c.usage_limit}` : ''}</td>
                    <td className="px-5 py-4">
                      <button
                        onClick={() => toggleActive(c)}
                        className={`badge ${c.is_active ? 'bg-green-400/10 text-green-400' : 'bg-gray-400/10 text-gray-400'}`}
                      >
                        {c.is_active ? 'Active' : 'Inactive'}
                      </button>
                    </td>
                    <td className="px-5 py-4">
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => openEdit(c)}
                          className="p-2 rounded-lg bg-ash-100 hover:bg-ash-200 text-gray-400 hover:text-white transition-colors"
                        >
                          <Pencil className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => handleDelete(c)}
                          className="p-2 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 transition-colors"
                        >
                          <Trash2 className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {coupons.length === 0 && (
              <div className="text-center py-16 text-gray-500">
                No coupons yet. Click "New Coupon" to create one.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

