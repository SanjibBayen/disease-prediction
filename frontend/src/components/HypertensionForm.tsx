import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Activity,
  Loader2,
  AlertCircle,
  Heart,
  User,
  Scale,
  Droplets,
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
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
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

const hypertensionSchema = z.object({
  male: z.coerce.number().min(0).max(1),
  age: z.coerce.number().min(32).max(70),
  cigsPerDay: z.coerce.number().min(0).max(70),
  BPMeds: z.coerce.number().min(0).max(1),
  totChol: z.coerce.number().min(107).max(500),
  sysBP: z.coerce.number().min(83.5).max(295),
  diaBP: z.coerce.number().min(48).max(142.5),
  BMI: z.coerce.number().min(15.54).max(56.8),
  heartRate: z.coerce.number().min(44).max(143),
  glucose: z.coerce.number().min(40).max(394),
});

type HypertensionFormValues = z.infer<typeof hypertensionSchema>;

export default function HypertensionForm() {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<HypertensionFormValues>({
    resolver: zodResolver(hypertensionSchema) as any,
    defaultValues: {
      male: 1,
      age: 50,
      cigsPerDay: 0,
      BPMeds: 0,
      totChol: 200,
      sysBP: 120,
      diaBP: 80,
      BMI: 24.5,
      heartRate: 72,
      glucose: 90,
    },
  });

  async function onSubmit(values: HypertensionFormValues) {
    setIsLoading(true);
    try {
      const response = await predictionService.predictHypertension(values);
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
        title="Hypertension Risk"
      />
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <Card className="border-none shadow-xl">
        <CardHeader className="bg-primary/5 border-b pb-6">
          <div className="flex items-center gap-3">
            <div className="bg-primary p-2 rounded-lg shadow-lg shadow-primary/20">
              <Activity className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <CardTitle className="text-2xl font-bold text-foreground">
                Hypertension Risk Assessment
              </CardTitle>
              <CardDescription className="text-muted-foreground">
                Clinical blood pressure and metabolic risk analysis
              </CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent className="pt-8">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <FormField
                  control={form.control}
                  name="male"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <User className="w-4 h-4 text-orange-500" /> Gender
                      </FormLabel>
                      <Select
                        onValueChange={(v) => field.onChange(parseInt(v))}
                        defaultValue={field.value.toString()}
                      >
                        <FormControl>
                          <SelectTrigger className="bg-slate-50 border-slate-200">
                            <SelectValue placeholder="Select gender" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="1">Male</SelectItem>
                          <SelectItem value="0">Female</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="age"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Age
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="BMI"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <Scale className="w-4 h-4 text-orange-500" /> BMI
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          step="0.1"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="sysBP"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Systolic BP
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Upper reading (mmHg)
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="diaBP"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Diastolic BP
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Lower reading (mmHg)
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="heartRate"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <Heart className="w-4 h-4 text-orange-500" /> Heart Rate
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="totChol"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Total Cholesterol
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="glucose"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <Droplets className="w-4 h-4 text-orange-500" /> Glucose
                        Level
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="cigsPerDay"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Cigarettes/Day
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="BPMeds"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        BP Medication
                      </FormLabel>
                      <Select
                        onValueChange={(v) => field.onChange(parseInt(v))}
                        defaultValue={field.value.toString()}
                      >
                        <FormControl>
                          <SelectTrigger className="bg-slate-50 border-slate-200">
                            <SelectValue placeholder="Select status" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="0">No</SelectItem>
                          <SelectItem value="1">Yes</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="pt-6 border-t border-slate-100">
                <Button
                  type="submit"
                  className="w-full h-12 bg-orange-600 hover:bg-orange-700 text-white font-bold text-lg rounded-xl shadow-lg shadow-orange-100 transition-all duration-200"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Analyzing Metabolic Data...
                    </>
                  ) : (
                    "Run Hypertension Analysis"
                  )}
                </Button>
                <div className="mt-4 flex items-center justify-center gap-2 text-slate-400">
                  <AlertCircle className="w-4 h-4" />
                  <span className="text-[10px] font-medium uppercase tracking-wider">
                    Clinical Data Privacy Guaranteed
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
