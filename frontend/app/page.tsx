"use client";

import { useState } from "react";
import Chat from "./components/Chat";
import Tickets from "./components/Tickets";
import { useUser } from "./contexts/UserContext";

export default function Home() {
  const [activeTab, setActiveTab] = useState<"chat" | "tickets">("chat");
  const { user, isLoading } = useUser();

  return (
    <div className="flex h-screen w-full flex-col overflow-hidden">
      {/* Navigation Tabs with User Info */}
      <div className="flex-shrink-0 border-b border-gray-200 bg-white shadow-sm dark:border-gray-700 dark:bg-gray-800">
        <div className="flex items-center justify-between px-4">
          <nav className="flex">
            <button
              onClick={() => setActiveTab("chat")}
              className={`flex items-center gap-2 border-b-2 px-4 sm:px-6 py-3 sm:py-4 text-sm font-medium transition-all ${
                activeTab === "chat"
                  ? "border-typhoon-primary text-typhoon-primary"
                  : "border-transparent text-gray-400 hover:border-rhythm hover:text-gray-300"
              }`}
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"
                />
              </svg>
              <span className="hidden sm:inline">IT Support Chat</span>
              <span className="sm:hidden">Chat</span>
            </button>
            <button
              onClick={() => setActiveTab("tickets")}
              className={`flex items-center gap-2 border-b-2 px-4 sm:px-6 py-3 sm:py-4 text-sm font-medium transition-all ${
                activeTab === "tickets"
                  ? "border-typhoon-primary text-typhoon-primary"
                  : "border-transparent text-gray-400 hover:border-rhythm hover:text-gray-300"
              }`}
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
              <span>Tickets</span>
            </button>
          </nav>

          {/* User Profile Display */}
          {!isLoading && user && (
            <div className="flex items-center gap-3 py-2">
              <div className="hidden lg:block text-right">
                <div className="text-xs text-gray-500 dark:text-gray-400 mb-1">
                  Logged in as{" "}
                  <span className="font-medium text-blue-600 dark:text-blue-400">
                    {user.nickname}
                  </span>
                </div>
                <div className="text-sm font-medium text-gray-900 dark:text-white">
                  {user.full_name_th}
                </div>
                <div className="text-xs text-gray-500 dark:text-gray-400">
                  {user.position} • {user.department}
                </div>
              </div>
              <div className="flex h-10 w-10 items-center justify-center rounded-full bg-gradient-to-br from-green-500 to-emerald-600 text-white shadow-lg ring-2 ring-green-200 dark:ring-green-900 font-bold">
                {user.nickname.charAt(0)}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 min-h-0 overflow-hidden">
        <div className={`h-full ${activeTab === "chat" ? "" : "hidden"}`}>
          <Chat />
        </div>
        <div className={`h-full ${activeTab === "tickets" ? "" : "hidden"}`}>
          <Tickets />
        </div>
      </div>
    </div>
  );
}
