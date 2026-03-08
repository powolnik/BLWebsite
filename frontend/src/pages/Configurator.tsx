import { useEffect } from 'react';
import { motion } from 'framer-motion';
import { useConfiguratorStore } from '../store/configuratorStore';
import ModulePicker from '../components/configurator/ModulePicker';
import SceneCanvas from '../components/configurator/SceneCanvas';
import SceneSummary from '../components/configurator/SceneSummary';
import Loader from '../components/ui/Loader';

export default function Configurator() {
  const { fetchData, isLoading, categories } = useConfiguratorStore();

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  if (isLoading || categories.length === 0) {
    return (
      <div className="grid-bg min-h-screen flex items-center justify-center">
        <Loader />
      </div>
    );
  }

  return (
    <div className="grid-bg min-h-screen pt-20 pb-8 px-4">
      <div className="max-w-[1600px] mx-auto">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-6"
        >
          <h1 className="text-3xl md:text-4xl font-bold">
            <span className="gradient-text">Konfigurator scen</span>
          </h1>
          <p className="text-[var(--color-text-secondary)] mt-2 text-sm max-w-xl mx-auto">
            Stwórz swoją własną scenę z modułów Black Light Collective.
            Wybierz elementy, zobacz wizualizację i złóż zamówienie.
          </p>
        </motion.div>

        {/* 3-column layout */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="grid grid-cols-1 lg:grid-cols-[320px_1fr_280px] gap-4"
          style={{ height: 'calc(100vh - 200px)', minHeight: '500px' }}
        >
          {/* Left: Module Picker */}
          <div className="order-2 lg:order-1 lg:h-full">
            <ModulePicker />
          </div>

          {/* Center: Scene Canvas */}
          <div className="order-1 lg:order-2 lg:h-full min-h-[300px]">
            <SceneCanvas />
          </div>

          {/* Right: Summary */}
          <div className="order-3 lg:h-full">
            <SceneSummary />
          </div>
        </motion.div>
      </div>
    </div>
  );
}
