"use client";

export default function DemoIndicator() {
  return (
    <div className="fixed bottom-4 left-4 z-50 animate-in fade-in slide-in-from-bottom-2 duration-700">
      <div className="flex items-center gap-2 rounded-xl border-2 border-blue-500 bg-white px-4 py-2 shadow-2xl backdrop-blur-sm dark:bg-gray-800 dark:border-blue-400">
        <div className="flex h-3 w-3 items-center justify-center">
          <span className="absolute inline-flex h-3 w-3 animate-ping rounded-full bg-blue-400 opacity-75"></span>
          <span className="relative inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
        </div>
        <div className="text-sm">
          <div className="font-semibold text-gray-900 dark:text-white">
            🎭 Demo Mode
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Logged in as <span className="font-medium text-blue-600 dark:text-blue-400">Somchai</span>
          </div>
        </div>
      </div>
    </div>
  );
}


