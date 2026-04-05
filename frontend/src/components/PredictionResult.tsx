import { useState, useRef } from "react";
import { motion } from "motion/react";
import {
  CheckCircle2,
  AlertCircle,
  AlertTriangle,
  Info,
  ArrowLeft,
  Download,
  Share2,
  Clock,
  Loader2,
} from "lucide-react";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";
import jsPDF from "jspdf";
import { domToPng } from "modern-screenshot";

interface PredictionResultProps {
  result: {
    success: boolean;
    prediction?: number;
    probability?: number;
    risk_level: string;
    message: string;
    recommendations: string[];
    timestamp: string;
    // Mental health specific
    depression_risk?: number;
    anxiety_risk?: number;
    // Sleep health specific
    sleep_score?: number | null;
    factors_affected?: string[] | null;
  };
  onReset: () => void;
  title: string;
}

export default function PredictionResult({
  result,
  onReset,
  title,
}: PredictionResultProps) {
  const [isExporting, setIsExporting] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);
  const isHighRisk = result.risk_level.toLowerCase() === "high";
  const isModerateRisk = result.risk_level.toLowerCase() === "moderate";

  const getRiskColor = () => {
    if (isHighRisk) return "text-red-700 bg-red-50/50 border-red-100";
    if (isModerateRisk) return "text-amber-700 bg-amber-50/50 border-amber-100";
    return "text-emerald-700 bg-emerald-50/50 border-emerald-100";
  };

  const getRiskIcon = () => {
    if (isHighRisk) return <AlertCircle className="w-6 h-6 text-red-600" />;
    if (isModerateRisk)
      return <AlertTriangle className="w-6 h-6 text-amber-600" />;
    return <CheckCircle2 className="w-6 h-6 text-emerald-600" />;
  };

  const handleExportPDF = async () => {
    if (!reportRef.current) return;

    setIsExporting(true);
    try {
      const element = reportRef.current;

      // Use modern-screenshot to get a high-quality PNG
      // It handles modern CSS like oklch much better than other libraries
      const dataUrl = await domToPng(element, {
        quality: 1,
        scale: 2,
        backgroundColor: "#f8fafc", // Matches bg-slate-50
      });

      const pdf = new jsPDF({
        orientation: "portrait",
        unit: "px",
        format: [element.offsetWidth, element.offsetHeight],
      });

      pdf.addImage(
        dataUrl,
        "PNG",
        0,
        0,
        element.offsetWidth,
        element.offsetHeight,
      );
      pdf.save(
        `Disease Prediction AI_${title.replace(/\s+/g, "_")}_Report.pdf`,
      );
    } catch (error) {
      console.error("PDF Export Error:", error);
    } finally {
      setIsExporting(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8 max-w-4xl mx-auto"
    >
      <div className="flex items-center justify-between border-b pb-4">
        <div className="flex flex-col">
          <h2 className="text-2xl font-bold text-foreground tracking-tight">
            {title} Analysis Report
          </h2>
          <p className="text-xs text-muted-foreground font-medium uppercase tracking-widest mt-1">
            Clinical Diagnostic Output
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="outline"
            size="sm"
            className="h-9 px-4 font-semibold"
            onClick={onReset}
          >
            <ArrowLeft className="w-4 h-4 mr-2" /> New Assessment
          </Button>
          <Button
            variant="default"
            size="sm"
            className="h-9 px-4 font-semibold shadow-lg shadow-primary/20"
            onClick={handleExportPDF}
            disabled={isExporting}
          >
            {isExporting ? (
              <Loader2 className="w-4 h-4 mr-2 animate-spin" />
            ) : (
              <Download className="w-4 h-4 mr-2" />
            )}
            Export PDF
          </Button>
        </div>
      </div>

      <div ref={reportRef} className="p-4 md:p-8 bg-slate-50 rounded-3xl">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2 space-y-8">
            <section className="space-y-4">
              <h3 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">
                Diagnostic Summary
              </h3>
              <div
                className={cn(
                  "p-6 rounded-2xl border-2 shadow-sm transition-all duration-500",
                  getRiskColor(),
                )}
              >
                <div className="flex items-start gap-5">
                  <div className="p-3 bg-white rounded-xl shadow-sm border border-inherit">
                    {getRiskIcon()}
                  </div>
                  <div className="space-y-2">
                    <div className="flex items-center gap-3">
                      <span className="text-lg font-bold">
                        Risk Level: {result.risk_level}
                      </span>
                      <Badge
                        variant="outline"
                        className="bg-white/50 border-inherit font-bold"
                      >
                        {Math.round(
                          result.probability || result.depression_risk || 0,
                        )}
                        % Confidence
                      </Badge>
                    </div>
                    <p className="text-sm leading-relaxed font-medium opacity-90">
                      {result.message}
                    </p>
                  </div>
                </div>
              </div>
            </section>

            <section className="space-y-4">
              <h3 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">
                Clinical Recommendations
              </h3>
              <div className="grid grid-cols-1 gap-3">
                {result.recommendations.map((rec, i) => (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.3 + i * 0.1 }}
                    className="bg-card p-4 rounded-xl border border-border flex gap-4 items-start hover:border-primary/30 transition-colors"
                  >
                    <div className="w-6 h-6 rounded-lg bg-primary/10 text-primary flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">
                      {i + 1}
                    </div>
                    <p className="text-sm text-foreground/80 font-medium leading-relaxed">
                      {rec}
                    </p>
                  </motion.div>
                ))}
              </div>
            </section>
          </div>

          <div className="space-y-8">
            <section className="space-y-4">
              <h3 className="text-sm font-bold text-muted-foreground uppercase tracking-wider">
                Metabolic Indicators
              </h3>
              <Card className="border-border bg-card/50 backdrop-blur-sm shadow-sm">
                <CardContent className="p-6 space-y-6">
                  {(result.probability !== undefined ||
                    result.depression_risk !== undefined) && (
                    <div className="space-y-3">
                      <div className="flex justify-between text-xs font-bold uppercase tracking-wider text-muted-foreground">
                        <span>Risk Probability</span>
                        <span className="text-foreground">
                          {Math.round(
                            result.probability || result.depression_risk || 0,
                          )}
                          %
                        </span>
                      </div>
                      <Progress
                        value={result.probability || result.depression_risk}
                        className="h-2 bg-muted"
                      />
                    </div>
                  )}

                  {result.anxiety_risk !== undefined && (
                    <div className="space-y-3">
                      <div className="flex justify-between text-xs font-bold uppercase tracking-wider text-muted-foreground">
                        <span>Anxiety Index</span>
                        <span className="text-foreground">
                          {Math.round(result.anxiety_risk)}%
                        </span>
                      </div>
                      <Progress
                        value={result.anxiety_risk}
                        className="h-2 bg-muted"
                      />
                    </div>
                  )}

                  {result.sleep_score !== undefined &&
                    result.sleep_score !== null && (
                      <div className="space-y-3">
                        <div className="flex justify-between text-xs font-bold uppercase tracking-wider text-muted-foreground">
                          <span>Sleep Quality Score</span>
                          <span className="text-foreground">
                            {result.sleep_score}/100
                          </span>
                        </div>
                        <Progress
                          value={result.sleep_score}
                          className="h-2 bg-muted"
                        />
                      </div>
                    )}

                  <div className="pt-4 border-t border-border">
                    <div className="flex items-center gap-2 text-[10px] text-muted-foreground font-medium">
                      <Clock className="w-3 h-3" />
                      Report generated on{" "}
                      {new Date(result.timestamp).toLocaleString()}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </section>

            <Card className="bg-muted/50 border-dashed border-2 border-muted-foreground/20">
              <CardContent className="p-6 text-center space-y-3">
                <div className="bg-muted p-3 rounded-full w-fit mx-auto">
                  <Info className="w-5 h-5 text-muted-foreground" />
                </div>
                <h4 className="text-sm font-bold text-foreground">
                  Medical Disclaimer
                </h4>
                <p className="text-[11px] text-muted-foreground leading-relaxed">
                  This analysis is for informational purposes only. It is not a
                  clinical diagnosis. Please consult with a qualified healthcare
                  professional for medical advice.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
