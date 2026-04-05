import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  Activity,
  Heart,
  Wind,
  Brain,
  Moon,
  Stethoscope,
  Menu,
  X,
  LayoutDashboard,
  Droplets,
  Zap,
  Shield,
  CheckCircle2,
  AlertCircle,
  Lock,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Toaster } from "@/components/ui/sonner";
import { cn } from "@/lib/utils";

// Prediction Components (to be created)
import DiabetesForm from "./components/DiabetesForm";
import AsthmaForm from "./components/AsthmaForm";
import CardioForm from "./components/CardioForm";
import StrokeForm from "./components/StrokeForm";
import HypertensionForm from "./components/HypertensionForm";
import SleepForm from "./components/SleepForm";
import MentalHealthForm from "./components/MentalHealthForm";
import Dashboard from "./components/Dashboard";

type PredictionType =
  | "dashboard"
  | "diabetes"
  | "asthma"
  | "cardio"
  | "stroke"
  | "hypertension"
  | "sleep"
  | "mental-health";

export default function App() {
  const [activeTab, setActiveTab] = useState<PredictionType>("dashboard");
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const menuItems = [
    {
      id: "dashboard",
      label: "Dashboard",
      icon: LayoutDashboard,
      color: "text-blue-500",
    },
    {
      id: "diabetes",
      label: "Diabetes Risk",
      icon: Droplets,
      color: "text-red-500",
    },
    {
      id: "cardio",
      label: "Cardiovascular",
      icon: Heart,
      color: "text-rose-500",
    },
    {
      id: "hypertension",
      label: "Hypertension",
      icon: Activity,
      color: "text-orange-500",
    },
    { id: "stroke", label: "Stroke Risk", icon: Zap, color: "text-purple-500" },
    {
      id: "asthma",
      label: "Asthma Assessment",
      icon: Wind,
      color: "text-cyan-500",
    },
    {
      id: "sleep",
      label: "Sleep Health",
      icon: Moon,
      color: "text-indigo-500",
    },
    {
      id: "mental-health",
      label: "Mental Health",
      icon: Brain,
      color: "text-pink-500",
    },
  ];

  const renderContent = () => {
    switch (activeTab) {
      case "dashboard":
        return <Dashboard onSelect={setActiveTab} />;
      case "diabetes":
        return <DiabetesForm />;
      case "asthma":
        return <AsthmaForm />;
      case "cardio":
        return <CardioForm />;
      case "stroke":
        return <StrokeForm />;
      case "hypertension":
        return <HypertensionForm />;
      case "sleep":
        return <SleepForm />;
      case "mental-health":
        return <MentalHealthForm />;
      default:
        return <Dashboard onSelect={setActiveTab} />;
    }
  };

  return (
    <div className="h-screen bg-slate-50 flex flex-col md:flex-row overflow-hidden">
      {/* Mobile Header */}
      <header className="md:hidden bg-background border-b px-4 py-3 flex items-center justify-between sticky top-0 z-50 shrink-0">
        <div className="flex items-center gap-2">
          <div className="bg-primary p-1.5 rounded-lg">
            <Stethoscope className="w-5 h-5 text-primary-foreground" />
          </div>
          <span className="font-bold text-foreground">
            Disease Prediction AI
          </span>
        </div>
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
        >
          {isSidebarOpen ? (
            <X className="text-foreground" />
          ) : (
            <Menu className="text-foreground" />
          )}
        </Button>
      </header>

      {/* Sidebar */}
      <aside
        className={cn(
          "fixed inset-0 z-40 bg-white border-r w-64 transform transition-transform duration-300 ease-in-out md:sticky md:top-0 md:h-screen md:translate-x-0 shrink-0",
          isSidebarOpen ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <div className="h-full flex flex-col">
          <div className="hidden md:flex items-center gap-3 px-6 py-8">
            <div className="bg-primary p-2 rounded-xl shadow-lg shadow-primary/20">
              <Stethoscope className="w-6 h-6 text-primary-foreground" />
            </div>
            <div className="flex flex-col">
              <span className="font-bold text-foreground leading-none tracking-tight text-lg">
                Disease Prediction AI
              </span>
              <span className="text-[10px] text-muted-foreground font-semibold tracking-widest uppercase mt-1">
                Clinical Suite
              </span>
            </div>
          </div>

          <nav className="flex-1 px-4 space-y-1 overflow-y-auto pb-4">
            {menuItems.map((item) => (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id as PredictionType);
                  setIsSidebarOpen(false);
                }}
                className={cn(
                  "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 group",
                  activeTab === item.id
                    ? "bg-primary/10 text-primary shadow-sm"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground",
                )}
              >
                <item.icon
                  className={cn(
                    "w-5 h-5 transition-colors",
                    activeTab === item.id
                      ? "text-primary"
                      : "text-muted-foreground/60 group-hover:text-foreground",
                  )}
                />
                {item.label}
              </button>
            ))}
          </nav>

          <div className="p-4 border-t bg-muted/30">
            <div className="flex items-center gap-3 px-2">
              <div className="w-2 h-2 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
              <div className="flex flex-col">
                <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-wider">
                  Clinical Engine
                </span>
                <span className="text-[10px] text-foreground/70 font-medium">
                  v3.0.0 Stable
                </span>
              </div>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative flex flex-col">
        <div className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 md:px-8 lg:px-12 py-8 md:py-12">
          <AnimatePresence mode="wait">
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
            >
              {renderContent()}
            </motion.div>
          </AnimatePresence>
        </div>

        {/* <footer className="w-full border-t border-slate-200 bg-white/50 backdrop-blur-sm mt-auto">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8 lg:px-12 py-12">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
              <div className="col-span-1 md:col-span-2 space-y-6">
                <div className="flex items-center gap-2">
                  <div className="bg-primary p-1.5 rounded-lg">
                    <Stethoscope className="w-4 h-4 text-primary-foreground" />
                  </div>
                  <span className="font-bold text-slate-900 tracking-tight">
                    Disease Prediction AI Clinical
                  </span>
                </div>
                <p className="text-xs text-slate-500 leading-relaxed max-w-md font-medium">
                  Disease Prediction AI is a clinical decision support platform
                  providing high-fidelity health risk assessments. Our models
                  are built on validated clinical datasets to assist healthcare
                  providers in early risk identification.
                </p>
                <div className="flex gap-4">
                  <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-400 hover:text-primary transition-colors cursor-pointer">
                    <Shield className="w-4 h-4" />
                  </div>
                  <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-400 hover:text-primary transition-colors cursor-pointer">
                    <Lock className="w-4 h-4" />
                  </div>
                  <div className="w-8 h-8 rounded-lg bg-slate-100 flex items-center justify-center text-slate-400 hover:text-primary transition-colors cursor-pointer">
                    <CheckCircle2 className="w-4 h-4" />
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h4 className="text-[10px] font-bold text-slate-900 uppercase tracking-[0.2em]">
                  Resources
                </h4>
                <nav className="flex flex-col gap-3">
                  <button className="text-xs text-slate-500 hover:text-primary font-medium transition-colors text-left">
                    Clinical Methodology
                  </button>
                  <button className="text-xs text-slate-500 hover:text-primary font-medium transition-colors text-left">
                    Model Validation
                  </button>
                  <button className="text-xs text-slate-500 hover:text-primary font-medium transition-colors text-left">
                    API Documentation
                  </button>
                </nav>
              </div>

              <div className="space-y-4">
                <h4 className="text-[10px] font-bold text-slate-900 uppercase tracking-[0.2em]">
                  Legal
                </h4>
                <nav className="flex flex-col gap-3">
                  <button className="text-xs text-slate-500 hover:text-primary font-medium transition-colors text-left">
                    Privacy Policy
                  </button>
                  <button className="text-xs text-slate-500 hover:text-primary font-medium transition-colors text-left">
                    Terms of Service
                  </button>
                  <button className="text-xs text-slate-500 hover:text-primary font-medium transition-colors text-left">
                    Compliance Standards
                  </button>
                </nav>
              </div>
            </div>

            <div className="mt-12 pt-8 border-t border-slate-100">
              <div className="bg-slate-50 rounded-2xl p-6 border border-slate-100">
                <div className="flex gap-4 items-start">
                  <AlertCircle className="w-5 h-5 text-slate-400 shrink-0 mt-0.5" />
                  <p className="text-[10px] text-slate-500 leading-relaxed font-medium">
                    <span className="font-bold text-slate-900 uppercase tracking-wider mr-2">
                      Legal Disclaimer:
                    </span>
                    Disease Prediction AI is intended for professional clinical
                    decision support and is not a substitute for professional
                    medical judgment, diagnosis, or treatment. The risk scores
                    generated are statistical probabilities and should be
                    interpreted within the context of a complete clinical
                    evaluation. In the event of a medical emergency, please
                    contact emergency services immediately.
                  </p>
                </div>
              </div>
              <div className="mt-8 flex flex-col sm:flex-row justify-between items-center gap-4">
                <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                  © 2026 Disease Prediction AI Clinical Suite. All rights
                  reserved.
                </p>
                <div className="flex items-center gap-2 text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                  <div className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                  System Status: Operational
                </div>
              </div>
            </div>
          </div>
        </footer> */}
      </main>

      <Toaster position="top-right" />
    </div>
  );
}
