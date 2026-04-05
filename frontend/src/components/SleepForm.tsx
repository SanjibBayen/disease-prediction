import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Moon,
  Loader2,
  AlertCircle,
  Clock,
  Activity,
  User,
  Briefcase,
  Scale,
  Heart,
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
import { SleepHealthResponse } from "@/types";
import PredictionResult from "./PredictionResult";
import { toast } from "sonner";

const sleepSchema = z.object({
  gender: z.string(),
  age: z.coerce.number().min(27).max(59),
  occupation: z.string(),
  sleep_duration: z.coerce.number().min(5.8).max(8.5),
  quality_of_sleep: z.coerce.number().min(4).max(9),
  physical_activity_level: z.coerce.number().min(30).max(90),
  stress_level: z.coerce.number().min(3).max(8),
  bmi_category: z.string(),
  blood_pressure: z
    .string()
    .regex(
      /^\d{2,3}\/\d{2,3}$/,
      "Format must be systolic/diastolic (e.g., 120/80)",
    ),
  heart_rate: z.coerce.number().min(65).max(86),
  daily_steps: z.coerce.number().min(3000).max(10000),
});

type SleepFormValues = z.infer<typeof sleepSchema>;

export default function SleepForm() {
  const [result, setResult] = useState<SleepHealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<SleepFormValues>({
    resolver: zodResolver(sleepSchema) as any,
    defaultValues: {
      gender: "Male",
      age: 35,
      occupation: "Software Engineer",
      sleep_duration: 7.2,
      quality_of_sleep: 7,
      physical_activity_level: 45,
      stress_level: 5,
      bmi_category: "Normal",
      blood_pressure: "120/80",
      heart_rate: 72,
      daily_steps: 7000,
    },
  });

  async function onSubmit(values: SleepFormValues) {
    setIsLoading(true);
    try {
      const response = await predictionService.predictSleep(values);
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
        title="Sleep Health"
      />
    );
  }

  return (
    <div className="max-w-3xl mx-auto">
      <Card className="border-none shadow-xl">
        <CardHeader className="bg-primary/5 border-b pb-6">
          <div className="flex items-center gap-3">
            <div className="bg-primary p-2 rounded-lg shadow-lg shadow-primary/20">
              <Moon className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <CardTitle className="text-2xl font-bold text-foreground">
                Sleep Health Analysis
              </CardTitle>
              <CardDescription className="text-muted-foreground">
                Clinical assessment of sleep architecture and quality metrics
              </CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent className="pt-8">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-8">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {/* Personal Info */}
                <FormField
                  control={form.control}
                  name="gender"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <User className="w-4 h-4 text-indigo-500" /> Gender
                      </FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger className="bg-slate-50 border-slate-200">
                            <SelectValue placeholder="Select gender" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="Male">Male</SelectItem>
                          <SelectItem value="Female">Female</SelectItem>
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
                  name="occupation"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <Briefcase className="w-4 h-4 text-indigo-500" />{" "}
                        Occupation
                      </FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger className="bg-slate-50 border-slate-200">
                            <SelectValue placeholder="Select occupation" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="Software Engineer">
                            Software Engineer
                          </SelectItem>
                          <SelectItem value="Doctor">Doctor</SelectItem>
                          <SelectItem value="Teacher">Teacher</SelectItem>
                          <SelectItem value="Business">Business</SelectItem>
                          <SelectItem value="Nurse">Nurse</SelectItem>
                          <SelectItem value="Accountant">Accountant</SelectItem>
                          <SelectItem value="Engineer">Engineer</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                {/* Sleep Metrics */}
                <FormField
                  control={form.control}
                  name="sleep_duration"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <Clock className="w-4 h-4 text-indigo-500" /> Duration
                        (hrs)
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
                  name="quality_of_sleep"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Quality (1-10)
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
                  name="stress_level"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold">
                        Stress (1-10)
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

                {/* Physical Metrics */}
                <FormField
                  control={form.control}
                  name="bmi_category"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <Scale className="w-4 h-4 text-indigo-500" /> BMI
                        Category
                      </FormLabel>
                      <Select
                        onValueChange={field.onChange}
                        defaultValue={field.value}
                      >
                        <FormControl>
                          <SelectTrigger className="bg-slate-50 border-slate-200">
                            <SelectValue placeholder="Select BMI" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          <SelectItem value="Normal">Normal</SelectItem>
                          <SelectItem value="Overweight">Overweight</SelectItem>
                          <SelectItem value="Obese">Obese</SelectItem>
                        </SelectContent>
                      </Select>
                      <FormMessage />
                    </FormItem>
                  )}
                />

                <FormField
                  control={form.control}
                  name="blood_pressure"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <Activity className="w-4 h-4 text-indigo-500" /> Blood
                        Pressure
                      </FormLabel>
                      <FormControl>
                        <Input
                          placeholder="120/80"
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
                  name="heart_rate"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel className="text-slate-700 font-semibold flex items-center gap-2">
                        <Heart className="w-4 h-4 text-indigo-500" /> Heart Rate
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
              </div>

              <div className="pt-6 border-t border-slate-100">
                <Button
                  type="submit"
                  className="w-full h-12 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-lg rounded-xl shadow-lg shadow-indigo-100 transition-all duration-200"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Analyzing Sleep Patterns...
                    </>
                  ) : (
                    "Run Sleep Diagnostic"
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
