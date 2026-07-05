import {
  BatteryCharging,
  Zap,
  Cpu,
  Wrench,
  Plug,
  PlugZap,
  Thermometer,
  CircuitBoard,
  Package,
} from '@lucide/vue'

const map = {
  Baterias: { icon: BatteryCharging, tint: 'text-electric-500 bg-electric-500/10' },
  Inversores: { icon: Zap, tint: 'text-emerald-accent bg-emerald-accent/10' },
  'Módulos Eletrônicos': { icon: Cpu, tint: 'text-violet-600 bg-violet-500/10' },
  'Motores Elétricos': { icon: Wrench, tint: 'text-amber-600 bg-amber-500/10' },
  'Conectores HV': { icon: Plug, tint: 'text-rose-600 bg-rose-500/10' },
  'Carregadores OBC': { icon: PlugZap, tint: 'text-cyan-600 bg-cyan-500/10' },
  'Suspensão e Freios': { icon: CircuitBoard, tint: 'text-slate-600 bg-slate-500/10' },
  'Refrig. Térmica': { icon: Thermometer, tint: 'text-sky-600 bg-sky-500/10' },
}

export function categoryVisual(nome) {
  return map[nome] || { icon: Package, tint: 'text-ink-500 bg-ink-500/10' }
}
