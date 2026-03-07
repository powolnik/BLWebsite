import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { authService } from '../services/auth';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import toast from 'react-hot-toast';

export default function Register() {
  const [f, setF] = useState({ username: '', email: '', password: '', password_confirm: '' });
  const [loading, setLoading] = useState(false); const nav = useNavigate();
  const upd = (k: string) => (e: React.ChangeEvent<HTMLInputElement>) => setF(prev => ({ ...prev, [k]: e.target.value }));
  const submit = async (e: React.FormEvent) => { e.preventDefault(); if (f.password !== f.password_confirm) { toast.error('Hasla nie pasuja'); return; } setLoading(true); try { await authService.register(f); toast.success('Konto utworzone!'); nav('/login'); } catch { toast.error('Blad rejestracji'); } finally { setLoading(false); } };
  return (
    <div className="grid-bg min-h-screen flex items-center justify-center px-4">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md p-8 rounded-2xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)]">
        <h1 className="text-2xl font-bold text-center mb-2">Rejestracja</h1>
        <form onSubmit={submit} className="space-y-4">
          <Input label="Login" value={f.username} onChange={upd('username')} required />
          <Input label="Email" type="email" value={f.email} onChange={upd('email')} required />
          <Input label="Haslo" type="password" value={f.password} onChange={upd('password')} required />
          <Input label="Powtorz haslo" type="password" value={f.password_confirm} onChange={upd('password_confirm')} required />
          <Button type="submit" size="lg" className="w-full" isLoading={loading}>Zarejestruj</Button>
        </form>
        <p className="mt-6 text-center text-sm text-[var(--color-text-secondary)]">Masz konto? <Link to="/login" className="text-[var(--color-neon-green)] hover:underline">Zaloguj</Link></p>
      </motion.div>
    </div>
  );
}
