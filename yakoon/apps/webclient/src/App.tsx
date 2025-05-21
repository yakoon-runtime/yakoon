import { useState } from "react";
import { InputBar } from "./components/InputBar";
import { ConsoleOutput } from "./components/ConsoleOutput";
import { sendCommand } from "./api/yakoon-api";

export default function App() {
  const [output, setOutput] = useState<string[]>([]);

  const handleSubmit = async (input: string) => {
    setOutput((prev) => [...prev, `> ${input}`]);
    const result = await sendCommand(input);
    setOutput((prev) => [...prev, result]);
  };

  return (
    <div className="max-w-3xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold text-center">Yakoon Webclient</h1>
      <ConsoleOutput lines={output} />
      <InputBar onSubmit={handleSubmit} />
    </div>
  );
}
