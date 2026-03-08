import { forwardRef, type ButtonHTMLAttributes } from 'react';
import { clsx } from 'clsx';

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'neon' | 'outline' | 'ghost'; size?: 'sm' | 'md' | 'lg'; isLoading?: boolean;
}

const Button = forwardRef<HTMLButtonElement, Props>(
  ({ variant = 'neon', size = 'md', isLoading, className, children, disabled, ...p }, ref) => {
    const v = { neon: 'btn-neon', outline: 'btn-outline', ghost: 'text-[var(--color-text-secondary)] hover:text-[var(--color-neon-green)]' };
    const s = { sm: 'text-xs py-1.5 px-3', md: 'text-sm py-2.5 px-5', lg: 'text-base py-3 px-8' };
    return (
      <button ref={ref} disabled={disabled || isLoading} className={clsx('inline-flex items-center justify-center font-medium transition-all rounded-lg disabled:opacity-50', v[variant], s[size], className)} {...p}>
        {isLoading && <svg className="animate-spin -ml-1 mr-2 h-4 w-4" viewBox="0 0 24 24" fill="none"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"/></svg>}
        {children}
      </button>
    );
  },
);
Button.displayName = 'Button';
export default Button;
