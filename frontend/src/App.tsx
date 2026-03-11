import { lazy, Suspense } from 'react';
import { Routes, Route } from 'react-router-dom';
import Layout from './components/layout/Layout';
import Home from './pages/Home';
import About from './pages/About';
import Portfolio from './pages/Portfolio';
import PortfolioDetail from './pages/PortfolioDetail';
import Shop from './pages/Shop';
import ProductDetail from './pages/ProductDetail';
import CartPage from './pages/CartPage';
import Contact from './pages/Contact';
import Login from './pages/Login';
import Register from './pages/Register';
import NotFound from './pages/NotFound';
import Loader from './components/ui/Loader';

// Lazy-load heavy pages (Three.js, SceneEngine, etc.)
const Configurator = lazy(() => import('./pages/Configurator'));
const SceneBuilder = lazy(() => import('./pages/SceneBuilder'));

function LazyFallback() {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <Loader />
    </div>
  );
}

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<Home />} />
        <Route path="/about" element={<About />} />
        <Route path="/portfolio" element={<Portfolio />} />
        <Route path="/portfolio/:slug" element={<PortfolioDetail />} />
        <Route path="/configurator" element={<Suspense fallback={<LazyFallback />}><Configurator /></Suspense>} />
        <Route path="/scene-builder" element={<Suspense fallback={<LazyFallback />}><SceneBuilder /></Suspense>} />
        <Route path="/shop" element={<Shop />} />
        <Route path="/shop/:slug" element={<ProductDetail />} />
        <Route path="/cart" element={<CartPage />} />
        <Route path="/contact" element={<Contact />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
