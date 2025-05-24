import { useState } from "react";

type Props = {
  onSubmit: (input: string) => void;
};

export function InputBar({ onSubmit }: Props) {
  const [input, setInput] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim()) {
      onSubmit(input.trim());
      setInput("");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2 p-2">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        className="flex-1 border-zinc-700 rounded p-2 bg-zinc-800 text-gray-100"
        placeholder="Befehl eingeben..."
        autoFocus
      />
      <button type="submit" className="px-4 py-2 bg-blue-600 text-white rounded">
        OK
      </button>
    </form>
  );
}
