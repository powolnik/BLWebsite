import type { ThreeElements } from '@react-three/fiber';

// React 19 uses React.JSX namespace instead of global JSX
declare module 'react' {
  namespace JSX {
    interface IntrinsicElements extends ThreeElements {}
  }
}

// Also augment global JSX for safety
declare global {
  namespace JSX {
    interface IntrinsicElements extends ThreeElements {}
  }
}
