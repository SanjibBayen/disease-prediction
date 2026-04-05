import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Droplets,
  Info,
  Loader2,
  AlertCircle,
  ChevronRight,
  ChevronLeft,
  ShieldCheck,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { predictionService } from "@/services/api";
import { PredictionResponse } from "@/types";
import PredictionResult from "./PredictionResult";
import { toast } from "sonner";

const diabetesSchema = z.object({
  pregnancies: z.coerce.number().min(0).max(20),
  glucose: z.coerce.number().min(0).max(300),
  blood_pressure: z.coerce.number().min(0).max(200),
  skin_thickness: z.coerce.number().min(0).max(100),
  insulin: z.coerce.number().min(0).max(900),
  bmi: z.coerce.number().min(0).max(70),
  diabetes_pedigree: z.coerce.number().min(0).max(2.5),
  age: z.coerce.number().min(1).max(120),
});

type DiabetesFormValues = z.infer<typeof diabetesSchema>;

export default function DiabetesForm() {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [step, setStep] = useState(1);

  const form = useForm<DiabetesFormValues>({
    resolver: zodResolver(diabetesSchema) as any,
    defaultValues: {
      pregnancies: 0,
      glucose: 100,
      blood_pressure: 80,
      skin_thickness: 20,
      insulin: 79,
      bmi: 25,
      diabetes_pedigree: 0.5,
      age: 30,
    },
  });

  async function onSubmit(values: DiabetesFormValues) {
    setIsLoading(true);
    try {
      const response = await predictionService.predictDiabetes(values);
      setResult(response);
      toast.success("Analysis complete");
    } catch (error) {
      console.error(error);
      toast.error("Failed to process prediction. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }

  if (result) {
    return (
      <PredictionResult
        result={result}
        onReset={() => setResult(null)}
        title="Diabetes Risk"
      />
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card className="border-none shadow-xl">
        <CardHeader className="bg-primary/5 border-b pb-6">
          <div className="flex items-center gap-3">
            <div className="bg-primary p-2 rounded-lg shadow-lg shadow-primary/20">
              <Droplets className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <CardTitle className="text-2xl font-bold text-foreground">
                Diabetes Risk Assessment
              </CardTitle>
              <CardDescription className="text-muted-foreground">
                Clinical metabolic analysis based on validated diagnostic
                parameters
              </CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent className="pt-8">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <FormField
                  control={form.control}
                  name="age"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-foreground font-bold">
                        Patient Age
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-muted/30 border-border focus:ring-primary"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="pregnancies"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-foreground font-bold">
                        Pregnancies
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-muted/30 border-border"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Total number of times pregnant
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="glucose"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-foreground font-bold">
                        Plasma Glucose
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-muted/30 border-border"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Concentration (mg/dL) - 2h oral test
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="blood_pressure"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-foreground font-bold">
                        Diastolic BP
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-muted/30 border-border"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Blood pressure reading (mmHg)
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="bmi"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-foreground font-bold">
                        Body Mass Index
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          step="0.1"
                          {...field}
                          className="bg-muted/30 border-border"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Weight (kg) / Height (m)²
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="insulin"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-foreground font-bold">
                        Serum Insulin
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-muted/30 border-border"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        2-Hour serum insulin (mu U/ml)
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="skin_thickness"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-foreground font-bold">
                        Skin Fold Thickness
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-muted/30 border-border"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Triceps skin fold thickness (mm)
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="diabetes_pedigree"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-foreground font-bold">
                        Pedigree Function
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          step="0.001"
                          {...field}
                          className="bg-muted/30 border-border"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Family history genetic factor (0.0 - 2.5)
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="pt-6 border-t border-border">
                <Button
                  type="submit"
                  className="w-full h-12 bg-primary hover:bg-primary/90 text-primary-foreground font-bold text-lg rounded-xl shadow-xl shadow-primary/20 transition-all duration-200"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Processing Clinical Data...
                    </>
                  ) : (
                    "Execute Diagnostic Analysis"
                  )}
                </Button>
                <div className="mt-4 flex items-center justify-center gap-2 text-muted-foreground">
                  <ShieldCheck className="w-4 h-4 text-emerald-500" />
                  <span className="text-[10px] font-bold uppercase tracking-widest">
                    Secure HIPAA-Compliant Processing
                  </span>
                </div>
              </div>
            </form>
          </Form>
        </CardContent>
      </Card>
    </div>
  );
}
