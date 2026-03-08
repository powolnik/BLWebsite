import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../hooks/useAuth';
import Button from '../components/ui/Button';
import Input from '../components/ui/Input';
import toast from 'react-hot-toast';

export default function Login() {
  const [u, setU] = useState(''); const [p, setP] = useState('');
  const { login, isLoading } = useAuth(); const nav = useNavigate();
  const submit = async (e: React.FormEvent) => { e.preventDefault(); try { await login(u, p); toast.success('Zalogowano!'); nav('/'); } catch { toast.error('Bledne dane'); } };
  return (
    <div className="grid-bg min-h-screen flex items-center justify-center px-4">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md p-8 rounded-2xl bg-[var(--color-dark-card)] border border-[var(--color-dark-border)]">
        <h1 className="text-2xl font-bold text-center mb-2">Logowanie</h1>
        <p className="text-sm text-[var(--color-text-secondary)] text-center mb-8">Witaj w BLACK LIGHT</p>
        <form onSubmit={submit} className="space-y-4">
          <Input label="Login" value={u} onChange={e => setU(e.target.value)} required />
          <Input label="Haslo" type="password" value={p} onChange={e => setP(e.target.value)} required />
          <Button type="submit" size="lg" className="w-full" isLoading={isLoading}>Zaloguj</Button>
        </form>
        <p className="mt-6 text-center text-sm text-[var(--color-text-secondary)]">Nie masz konta? <Link to="/register" className="text-[var(--color-neon-green)] hover:underline">Zarejestruj sie</Link></p>
      </motion.div>
    </div>
  );
}
