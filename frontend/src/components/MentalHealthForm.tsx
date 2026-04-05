import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import {
  Brain,
  Loader2,
  AlertCircle,
  MessageSquare,
  Sparkles,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
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
import { MentalHealthResponse } from "@/types";
import PredictionResult from "./PredictionResult";
import { toast } from "sonner";

const mentalHealthSchema = z.object({
  text: z
    .string()
    .min(10, "Please provide more detail (at least 10 characters)")
    .max(5000),
});

type MentalHealthFormValues = z.infer<typeof mentalHealthSchema>;

export default function MentalHealthForm() {
  const [result, setResult] = useState<MentalHealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<MentalHealthFormValues>({
    resolver: zodResolver(mentalHealthSchema),
    defaultValues: {
      text: "",
    },
  });

  async function onSubmit(values: MentalHealthFormValues) {
    setIsLoading(true);
    try {
      const response = await predictionService.predictMentalHealth(values);
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
        title="Mental Health"
      />
    );
  }

  return (
    <div className="max-w-2xl mx-auto">
      <Card className="border-none shadow-xl">
        <CardHeader className="bg-primary/5 border-b pb-6">
          <div className="flex items-center gap-3">
            <div className="bg-primary p-2 rounded-lg shadow-lg shadow-primary/20">
              <Brain className="w-6 h-6 text-primary-foreground" />
            </div>
            <div>
              <CardTitle className="text-2xl font-bold text-foreground">
                Mental Health Screening
              </CardTitle>
              <CardDescription className="text-muted-foreground">
                Clinical NLP-based analysis for depression and anxiety risk
              </CardDescription>
            </div>
          </div>
        </CardHeader>

        <CardContent className="pt-8">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="text"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel className="text-foreground font-bold flex items-center gap-2">
                      <MessageSquare className="w-4 h-4 text-primary" />
                      Clinical Symptom Description
                    </FormLabel>
                    <FormControl>
                      <textarea
                        {...field}
                        className="w-full min-h-[200px] p-4 rounded-xl border border-border bg-muted/30 focus:ring-2 focus:ring-primary focus:border-transparent outline-none transition-all duration-200 text-foreground font-medium placeholder:text-muted-foreground/50"
                        placeholder="Please describe your current emotional state, sleep patterns, and any specific symptoms you've been experiencing..."
                      />
                    </FormControl>
                    <FormDescription className="text-xs text-slate-500">
                      Our AI analyzes linguistic patterns, sentiment, and
                      symptom descriptions to assess risk levels.
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <div className="bg-blue-50 p-4 rounded-xl border border-blue-100 flex gap-3 items-start">
                <Sparkles className="w-5 h-5 text-blue-500 shrink-0 mt-0.5" />
                <p className="text-xs text-blue-700 font-medium leading-relaxed">
                  Tip: Be as specific as possible about your feelings, physical
                  symptoms, and duration. The more detail you provide, the more
                  accurate the screening will be.
                </p>
              </div>

              <div className="pt-6 border-t border-slate-100">
                <Button
                  type="submit"
                  className="w-full h-12 bg-pink-600 hover:bg-pink-700 text-white font-bold text-lg rounded-xl shadow-lg shadow-pink-100 transition-all duration-200"
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                      Analyzing Text Patterns...
                    </>
                  ) : (
                    "Run Sentiment Analysis"
                  )}
                </Button>
                <div className="mt-4 flex items-center justify-center gap-2 text-slate-400">
                  <AlertCircle className="w-4 h-4" />
                  <span className="text-[10px] font-medium uppercase tracking-wider">
                    Confidential & Secure Processing
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
