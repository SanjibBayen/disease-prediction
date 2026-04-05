import { motion } from "motion/react";
import {
  Activity,
  Heart,
  Wind,
  Brain,
  Moon,
  Droplets,
  Zap,
  ChevronRight,
  ShieldCheck,
  Clock,
  Stethoscope,
  AlertCircle,
  FileText,
  Shield,
  CheckCircle2,
  Lock,
  ArrowRight,
  Database,
  Cpu,
  LineChart,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface DashboardProps {
  onSelect: (tab: any) => void;
}

export default function Dashboard({ onSelect }: DashboardProps) {
  const capabilities = [
    {
      label: "Diagnostic Suite",
      value: "7 Active Modules",
      icon: Activity,
      color: "text-blue-600",
    },
    {
      label: "Data Privacy",
      value: "Local Processing",
      icon: Lock,
      color: "text-emerald-600",
    },
    {
      label: "Analysis Speed",
      value: "Instant Response",
      icon: Zap,
      color: "text-amber-600",
    },
    {
      label: "Model Status",
      value: "Validated v3.0",
      icon: CheckCircle2,
      color: "text-indigo-600",
    },
  ];

  const tests = [
    {
      id: "diabetes",
      title: "Diabetes Risk",
      desc: "Metabolic analysis of plasma glucose, insulin levels, and BMI parameters.",
      icon: Droplets,
      color: "text-red-600",
    },
    {
      id: "cardio",
      title: "Cardiovascular",
      icon: Heart,
      desc: "Heart health assessment using blood pressure, cholesterol, and lifestyle metrics.",
      color: "text-rose-600",
    },
    {
      id: "hypertension",
      title: "Hypertension",
      icon: Activity,
      desc: "Screening for high blood pressure risk based on clinical and demographic data.",
      color: "text-orange-600",
    },
    {
      id: "stroke",
      title: "Stroke Risk",
      icon: Zap,
      desc: "Neurological evaluation of vascular risk factors and metabolic indicators.",
      color: "text-purple-600",
    },
    {
      id: "asthma",
      title: "Asthma Assessment",
      icon: Wind,
      desc: "Respiratory function analysis based on peak flow and environmental factors.",
      color: "text-cyan-600",
    },
    {
      id: "sleep",
      title: "Sleep Health",
      icon: Moon,
      desc: "Physiological assessment of sleep architecture and disorder risk levels.",
      color: "text-indigo-600",
    },
    {
      id: "mental-health",
      title: "Mental Health",
      icon: Brain,
      desc: "Clinical NLP screening for depression and anxiety symptom patterns.",
      color: "text-pink-600",
    },
  ];

  return (
    <div className="space-y-12 pb-20">
      {/* Medical Disclaimer Banner */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex gap-4 items-start shadow-sm"
      >
        <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <h4 className="text-sm font-bold text-amber-900 uppercase tracking-wider">
            Medical Disclaimer
          </h4>
          <p className="text-xs text-amber-800 leading-relaxed font-medium">
            Disease Prediction AI is a clinical decision support tool designed
            for informational purposes only. It does not provide medical
            diagnoses or treatment recommendations. Always seek the advice of a
            physician or other qualified health provider with any questions you
            may have regarding a medical condition.
          </p>
        </div>
      </motion.div>

      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-8">
        <div className="space-y-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/10 text-primary font-bold text-[10px] uppercase tracking-[0.2em]">
            <Shield className="w-3 h-3" />
            Clinical Intelligence v3.0
          </div>
          <h1 className="text-4xl sm:text-5xl font-black tracking-tight text-slate-900">
            Diagnostic Dashboard
          </h1>
          <p className="text-slate-500 max-w-xl text-lg font-medium leading-relaxed">
            Evidence-based health risk assessments powered by validated clinical
            data models and predictive analytics.
          </p>
        </div>

        <div className="flex items-center gap-4 bg-muted/50 p-2 rounded-lg border border-border">
          <div className="flex flex-col items-end px-3">
            <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">
              System Status
            </span>
            <span className="text-xs font-bold text-emerald-600 flex items-center gap-1.5">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              Operational
            </span>
          </div>
          <div className="w-px h-8 bg-border" />
          <div className="flex flex-col items-end px-3">
            <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest">
              Last Update
            </span>
            <span className="text-xs font-bold text-foreground">
              05 APR 2026
            </span>
          </div>
        </div>
      </div>

      {/* Diagnostic Modules Grid */}
      <div className="space-y-8">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-200 pb-6">
          <div className="space-y-1">
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
              Diagnostic Modules
            </h2>
            <p className="text-sm text-slate-500 font-medium">
              Select a specialized module for clinical evaluation
            </p>
          </div>
          <div className="flex items-center gap-4 text-[10px] font-bold text-slate-400 uppercase tracking-widest">
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-emerald-500" />
              Validated
            </div>
            <div className="flex items-center gap-1.5">
              <div className="w-2 h-2 rounded-full bg-blue-500" />
              Encrypted
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {tests.map((test, index) => (
            <motion.div
              key={test.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              whileHover={{ y: -4 }}
              className="group relative"
              onClick={() => onSelect(test.id)}
            >
              <Card className="h-full border-slate-200 hover:border-primary/30 hover:shadow-xl hover:shadow-primary/5 transition-all duration-300 cursor-pointer overflow-hidden bg-white">
                <CardContent className="p-0">
                  <div className="p-6 space-y-4">
                    <div className="flex justify-between items-start">
                      <div
                        className={cn(
                          "p-3 rounded-xl bg-slate-50 group-hover:bg-primary/10 transition-colors",
                          test.color,
                        )}
                      >
                        <test.icon className="w-6 h-6" />
                      </div>
                      <div className="flex items-center gap-1.5 px-2 py-1 rounded-full bg-slate-50 border border-slate-100">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
                        <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">
                          Active
                        </span>
                      </div>
                    </div>

                    <div>
                      <h3 className="text-lg font-bold text-slate-900 tracking-tight group-hover:text-primary transition-colors">
                        {test.title}
                      </h3>
                      <p className="text-sm text-slate-500 leading-relaxed mt-1 line-clamp-2 font-medium">
                        {test.desc}
                      </p>
                    </div>

                    <div className="pt-4 flex items-center justify-between border-t border-slate-50">
                      <div className="flex items-center gap-2 text-xs font-bold text-slate-400 uppercase tracking-widest">
                        <Clock className="w-3.5 h-3.5" />
                        <span>~2 min</span>
                      </div>
                      <div className="flex items-center gap-1 text-primary font-bold text-xs uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-all transform translate-x-2 group-hover:translate-x-0">
                        Launch Module
                        <ChevronRight className="w-4 h-4" />
                      </div>
                    </div>
                  </div>

                  {/* Subtle accent bar */}
                  <div className="h-1 w-full bg-gradient-to-r from-transparent via-slate-100 to-transparent opacity-50" />
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>

      {/* Methodology & Clinical Standards */}
      <section className="space-y-8 pt-8">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="space-y-2">
            <h2 className="text-2xl font-bold text-slate-900 tracking-tight">
              Clinical Methodology
            </h2>
            <p className="text-slate-500 font-medium max-w-2xl">
              Our predictive engines are built on peer-reviewed clinical
              datasets and validated against real-world health outcomes.
            </p>
          </div>
          <button className="flex items-center gap-2 text-xs font-bold text-primary uppercase tracking-widest hover:underline decoration-2 underline-offset-4">
            View Whitepapers <ChevronRight className="w-4 h-4" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {capabilities.map((cap, idx) => (
            <Card
              key={idx}
              className="border-slate-100 bg-slate-50/50 shadow-none"
            >
              <CardContent className="p-6 flex items-center gap-4">
                <div
                  className={cn(
                    "p-2.5 rounded-lg bg-white shadow-sm",
                    cap.color,
                  )}
                >
                  <cap.icon className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                    {cap.label}
                  </p>
                  <p className="text-lg font-bold text-slate-900 tracking-tight">
                    {cap.value}
                  </p>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card className="lg:col-span-2 border-slate-200 bg-white overflow-hidden">
            <CardContent className="p-8">
              <div className="flex flex-col md:flex-row gap-8 items-center">
                <div className="flex-1 space-y-4 text-center md:text-left">
                  <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 text-blue-700 text-[10px] font-bold uppercase tracking-wider border border-blue-100">
                    <ShieldCheck className="w-3 h-3" />
                    HIPAA Compliant Infrastructure
                  </div>
                  <h3 className="text-xl font-bold text-slate-900 tracking-tight">
                    Enterprise-Grade Security
                  </h3>
                  <p className="text-sm text-slate-500 leading-relaxed font-medium">
                    All diagnostic data is processed using end-to-end
                    encryption. Disease Prediction AI does not store personally
                    identifiable information (PII) on its prediction servers,
                    ensuring maximum patient privacy and compliance with global
                    healthcare standards.
                  </p>
                  <div className="flex flex-wrap justify-center md:justify-start gap-4 pt-2">
                    <div className="flex items-center gap-1.5 text-xs font-bold text-slate-600">
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                      AES-256 Encryption
                    </div>
                    <div className="flex items-center gap-1.5 text-xs font-bold text-slate-600">
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                      SOC2 Type II
                    </div>
                  </div>
                </div>
                <div className="w-full md:w-48 h-48 bg-slate-50 rounded-3xl flex items-center justify-center border border-slate-100 relative overflow-hidden group">
                  <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent" />
                  <Lock className="w-16 h-16 text-slate-200 group-hover:text-primary/20 transition-colors duration-500" />
                  <div className="absolute bottom-4 left-4 right-4 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                    <motion.div
                      className="h-full bg-primary"
                      initial={{ width: "0%" }}
                      animate={{ width: "100%" }}
                      transition={{ duration: 2, repeat: Infinity }}
                    />
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="border-primary/20 bg-primary/5 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-4 opacity-10">
              <Zap className="w-24 h-24 text-primary" />
            </div>
            <CardContent className="p-8 space-y-6 relative z-10">
              <h3 className="text-xl font-bold text-slate-900 tracking-tight">
                Continuous Learning
              </h3>
              <p className="text-sm text-slate-600 leading-relaxed font-medium">
                Our models are updated quarterly with the latest clinical
                research and epidemiological data to maintain industry-leading
                predictive accuracy.
              </p>
              <ul className="space-y-3">
                {[
                  "Latest WHO Guidelines",
                  "New Clinical Trials",
                  "Regional Health Data",
                ].map((item, i) => (
                  <li
                    key={i}
                    className="flex items-center gap-2 text-xs font-bold text-slate-700"
                  >
                    <div className="w-1 h-1 rounded-full bg-primary" />
                    {item}
                  </li>
                ))}
              </ul>
              <button className="w-full py-3 bg-white border border-primary/20 rounded-xl text-xs font-bold text-primary uppercase tracking-widest hover:bg-primary hover:text-white transition-all">
                View Update Log
              </button>
            </CardContent>
          </Card>
        </div>
      </section>
    </div>
  );
}
