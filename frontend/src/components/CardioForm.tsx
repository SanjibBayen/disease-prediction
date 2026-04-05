import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Heart,
  Loader2,
  AlertCircle,
  Activity,
  Scale,
  Zap,
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

const cardioSchema = z.object({
  active: z.coerce.number().min(0).max(1),
  age: z.coerce.number().min(29).max(65),
  alco: z.coerce.number().min(0).max(1),
  ap_hi: z.coerce.number().min(90).max(200),
  ap_lo: z.coerce.number().min(60).max(140),
  cholesterol: z.coerce.number().min(1).max(3),
  gluc: z.coerce.number().min(1).max(3),
  smoke: z.coerce.number().min(0).max(1),
  weight: z.coerce.number().min(30).max(200),
});

type CardioFormValues = z.infer<typeof cardioSchema>;

export default function CardioForm() {
  const [result, setResult] = useState<PredictionResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<CardioFormValues>({
    resolver: zodResolver(cardioSchema) as any,
    defaultValues: {
      active: 1,
      age: 45,
      alco: 0,
      ap_hi: 120,
      ap_lo: 80,
      cholesterol: 1,
      gluc: 1,
      smoke: 0,
      weight: 75,
    },
  });

  async function onSubmit(values: CardioFormValues) {
    setIsLoading(true);
    try {
      const response = await predictionService.predictCardio(values);
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
        title="Cardiovascular Risk"
      />
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card className="border-none shadow-xl">
        <CardHeader className="bg-primary/5 border-b pb-6">
          <div className="flex items-center gap-3">
            <div className="bg-primary p-2 rounded-lg shadow-lg shadow-primary/20">
              <Heart className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <CardTitle className="text-2xl font-bold text-foreground">
                Cardiovascular Risk Assessment
              </CardTitle>
              <CardDescription className="text-muted-foreground">
                Clinical heart health analysis based on validated diagnostic
                factors
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
                      <FormLabel className="text-slate-700 font-semibold">
                        Age (Years)
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
                  name="weight"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <Scale className="w-4 h-4 text-rose-500" /> Weight (kg)
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
                  name="ap_hi"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Systolic BP (ap_hi)
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Upper blood pressure reading
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="ap_lo"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Diastolic BP (ap_lo)
                      </FormLabel>
                      <FormControl>
                        <Input
                          type="number"
                          {...field}
                          className="bg-slate-50 border-slate-200"
                        />
                      </FormControl>
                      <FormDescription className="text-[10px]">
                        Lower blood pressure reading
                      </FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="cholesterol"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Cholesterol Level
                      </FormLabel>
                      <Select
                        onValueChange={(v) => field.onChange(parseInt(v))}
                        defaultValue={field.value.toString()}
                      >
                        <FormControl>
                          <SelectTrigger className="bg-slate-50 border-slate-200">
                            <SelectValue placeholder="Select level" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="1">Normal</SelectItem>
                          <SelectItem value="2">Above Normal</SelectItem>
                          <SelectItem value="3">Well Above Normal</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="gluc"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Glucose Level
                      </FormLabel>
                      <Select
                        onValueChange={(v) => field.onChange(parseInt(v))}
                        defaultValue={field.value.toString()}
                      >
                        <FormControl>
                          <SelectTrigger className="bg-slate-50 border-slate-200">
                            <SelectValue placeholder="Select level" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="1">Normal</SelectItem>
                          <SelectItem value="2">Above Normal</SelectItem>
                          <SelectItem value="3">Well Above Normal</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="smoke"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Smoking Status
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
                          <SelectItem value="0">Non-Smoker</SelectItem>
                          <SelectItem value="1">Smoker</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="active"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Physical Activity
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
                          <SelectItem value="0">Inactive</SelectItem>
                          <SelectItem value="1">Active</SelectItem>
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
                  className="w-full h-12 bg-rose-600 hover:bg-rose-700 text-white font-bold text-lg rounded-xl shadow-lg shadow-rose-100 transition-all duration-200"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Analyzing Cardiac Data...
                    </>
                  ) : (
                    "Run Cardiac Analysis"
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
