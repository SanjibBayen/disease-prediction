import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Wind,
  Loader2,
  AlertCircle,
  User,
  Activity,
  Info,
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

const asthmaSchema = z.object({
  gender_male: z.coerce.number().min(0).max(1),
  smoking_ex: z.coerce.number().min(0).max(1),
  smoking_non: z.coerce.number().min(0).max(1),
  age: z.coerce.number().min(0).max(1),
  peak_flow: z.coerce.number().min(0.1).max(1),
});

type AsthmaFormValues = z.infer<typeof asthmaSchema>;

export default function AsthmaForm() {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<AsthmaFormValues>({
    resolver: zodResolver(asthmaSchema) as any,
    defaultValues: {
      gender_male: 1,
      smoking_ex: 0,
      smoking_non: 1,
      age: 0.5,
      peak_flow: 0.6,
    },
  });

  async function onSubmit(values: AsthmaFormValues) {
    setIsLoading(true);
    try {
      const response = await predictionService.predictAsthma(values);
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
        title="Asthma Risk"
      />
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card className="border-none shadow-xl">
        <CardHeader className="bg-primary/5 border-b pb-6">
          <div className="flex items-center gap-3">
            <div className="bg-primary p-2 rounded-lg shadow-lg shadow-primary/20">
              <Wind className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <CardTitle className="text-2xl font-bold text-foreground">
                Asthma Risk Assessment
              </CardTitle>
              <CardDescription className="text-muted-foreground">
                Clinical respiratory function and lifestyle analysis
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
                  name="gender_male"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-foreground font-bold flex items-center gap-2">
                        <User className="w-4 h-4 text-primary" /> Biological Sex
                      </FormLabel>
                      <Select
                        onValueChange={(v) => field.onChange(parseInt(v))}
                        defaultValue={field.value.toString()}
                      >
                        <FormControl>
                          <SelectTrigger className="bg-muted/30 border-border">
                            <SelectValue placeholder="Select sex" />
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
                        Normalized Age (0-1)
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          step="0.01"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Age scaled between 0 and 1
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="peak_flow"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <Activity className="w-4 h-4 text-cyan-500" /> Peak Flow
                        Rate
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          step="0.01"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        L/sec (0.1 - 1.0)
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="smoking_non"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Non-Smoker Status
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
                          <SelectItem value="1">Yes</SelectItem>
                          <SelectItem value="0">No</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="smoking_ex"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Ex-Smoker Status
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
                          <SelectItem value="1">Yes</SelectItem>
                          <SelectItem value="0">No</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>

              <div className="bg-blue-50 p-4 rounded-xl border border-blue-100 flex gap-3 items-start">
                <Info className="w-5 h-5 text-blue-500 shrink-0 mt-0.5" />
                <p className="text-xs text-blue-700 font-medium leading-relaxed">
                  Peak Flow Rate is a measure of how fast you can breathe out.
                  It is a key indicator of respiratory health and asthma
                  control.
                </p>
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
                      Analyzing Clinical Data...
                    </>
                  ) : (
                    "Execute Diagnostic Analysis"
                  )}
                </Button>
                <div className="mt-4 flex items-center justify-center gap-2 text-muted-foreground">
                  <ShieldCheck className="w-4 h-4 text-emerald-500" />
                  <span className="text-[10px] font-bold uppercase tracking-widest">
                    Secure Clinical Data Processing
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
