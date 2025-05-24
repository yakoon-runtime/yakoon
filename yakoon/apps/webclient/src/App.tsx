import { useState, useRef, useEffect } from "react";
import { InputBar } from "./components/InputBar";
import { ConsoleOutput } from "./components/ConsoleOutput";
import { sendCommand } from "./api/yakoon-api";

export default function App() {
  const [output, setOutput] = useState<string[]>([]);
  const containerRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async (input: string) => {
    setOutput((prev) => [...prev, `> ${input}`]);
    const result = await sendCommand(input);
    setOutput((prev) => [...prev, result]);
  };

  useEffect(() => {
    // Scroll automatisch zum neuesten Output
    containerRef.current?.scrollTo(0, containerRef.current.scrollHeight);
  }, [output]);

  return (
    <div className="flex flex-col h-screen bg-zinc-900 text-gray-100">
      <div ref={containerRef} className="flex-1 overflow-y-auto p-4">
        <ConsoleOutput lines={output} />
      </div>
      <div className="border-t border-gray-700 p-4">
        <InputBar onSubmit={handleSubmit} />
      </div>
    </div>
  );
}
