import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Trash2, Minus, Plus, ShoppingBag } from 'lucide-react';
import { useCart } from '../hooks/useCart';
import Button from '../components/ui/Button';
import Loader from '../components/ui/Loader';

export default function CartPage() {
  const { cart, isLoading, updateQuantity, clearCart } = useCart();
  if (isLoading) return <Loader />;
  if (!cart || cart.items.length === 0) return (
    <div className="grid-bg py-24 px-4 text-center"><ShoppingBag className="w-16 h-16 mx-auto text-[var(--color-text-secondary)] mb-4" /><h1 className="text-2xl font-bold mb-2">Koszyk pusty</h1><Link to="/shop"><Button>Do sklepu</Button></Link></div>
  );
  return (
    <div className="grid-bg py-24 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8">Koszyk ({cart.item_count})</h1>
        <div className="space-y-4 mb-8">
          {cart.items.map(item => (
            <motion.div key={item.id} layout className="flex items-center gap-4 p-4 rounded-xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)]">
              {item.product_image && <img src={item.product_image} alt={item.product_name} className="w-20 h-20 rounded-lg object-cover" />}
              <div className="flex-1 min-w-0"><h3 className="font-medium truncate">{item.product_name}</h3><p className="text-sm text-[var(--color-text-secondary)]">{item.product_price} PLN</p></div>
              <div className="flex items-center gap-2"><button onClick={() => updateQuantity(item.id, item.quantity - 1)} className="p-1"><Minus className="w-4 h-4" /></button><span className="w-8 text-center">{item.quantity}</span><button onClick={() => updateQuantity(item.id, item.quantity + 1)} className="p-1"><Plus className="w-4 h-4" /></button></div>
              <span className="font-bold neon-text w-24 text-right">{item.subtotal} PLN</span>
              <button onClick={() => updateQuantity(item.id, 0)} className="hover:text-[var(--color-neon-pink)]"><Trash2 className="w-4 h-4" /></button>
            </motion.div>
          ))}
        </div>
        <div className="flex justify-between items-center p-6 rounded-xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)]">
          <div><span className="text-[var(--color-text-secondary)]">Razem:</span><span className="text-2xl font-bold neon-text ml-4">{cart.total} PLN</span></div>
          <div className="flex gap-3"><Button variant="ghost" onClick={clearCart}>Wyczysc</Button><Button size="lg">Do kasy</Button></div>
        </div>
      </div>
    </div>
  );
}
