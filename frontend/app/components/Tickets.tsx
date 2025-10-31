"use client";

import { useState, useEffect, useCallback, useMemo } from "react";
import { useUser } from "../contexts/UserContext";

interface Ticket {
  id: number;
  subject: string;
  description: string;
  status: "new" | "open" | "pending" | "solved" | "closed";
  priority: "low" | "normal" | "high" | "urgent";
  requester_name: string;
  requester_email: string;
  created_at: string;
  updated_at: string;
  comments: Comment[];
  assignee_id: string | null;
  assignee_name: string | null;
  tags: string[];
  category: string;
  due_date: string | null;
  first_response_at: string | null;
  resolved_at: string | null;
  sla_first_response_due: string;
  sla_resolution_due: string;
  sla_breach: {
    first_response_breached: boolean;
    resolution_breached: boolean;
  };
  history: HistoryEntry[];
}

interface Comment {
  author: string;
  body: string;
  public: boolean;
  created_at: string;
}

interface HistoryEntry {
  timestamp: string;
  action: string;
  actor: string;
  changes: any;
}

interface TicketStats {
  total: number;
  by_status: Record<string, number>;
  by_priority: Record<string, number>;
}

interface Agent {
  id: string;
  name: string;
  email: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const STATUS_COLORS = {
  new: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
  open: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
  pending: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200",
  solved: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
  closed: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200",
};

const PRIORITY_COLORS = {
  low: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200",
  normal: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
  high: "bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200",
  urgent: "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
};

const CATEGORY_LABELS: Record<string, string> = {
  hardware: "ฮาร์ดแวร์",
  software: "ซอฟต์แวร์",
  network: "เครือข่าย",
  account_access: "บัญชี/สิทธิ์",
  email: "อีเมล",
  printer: "เครื่องพิมพ์",
  vpn: "VPN",
  security: "ความปลอดภัย",
  other: "อื่นๆ",
};

export default function Tickets() {
  const { user } = useUser();
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [stats, setStats] = useState<TicketStats | null>(null);
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [priorityFilter, setPriorityFilter] = useState<string>("all");
  const [categoryFilter, setCategoryFilter] = useState<string>("all");
  const [assigneeFilter, setAssigneeFilter] = useState<string>("all");
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [isCreating, setIsCreating] = useState(false);
  const [showSuccessNotification, setShowSuccessNotification] = useState(false);
  const [createdTicket, setCreatedTicket] = useState<Ticket | null>(null);
  const [agents, setAgents] = useState<Agent[]>([]);
  const [selectedTickets, setSelectedTickets] = useState<Set<number>>(new Set());
  const [showBulkActions, setShowBulkActions] = useState(false);
  const [showHistoryModal, setShowHistoryModal] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<"created_at" | "updated_at" | "priority" | "status">("created_at");
  const [sortOrder, setSortOrder] = useState<"asc" | "desc">("desc");
  const [showQuickActions, setShowQuickActions] = useState(false);

  const fetchTickets = useCallback(async () => {
    setIsLoading(true);
    const params = new URLSearchParams();
    if (statusFilter !== "all") params.append("status", statusFilter);
    if (priorityFilter !== "all") params.append("priority", priorityFilter);
    if (categoryFilter !== "all") params.append("category", categoryFilter);
    if (assigneeFilter !== "all") params.append("assignee_id", assigneeFilter);
    
    const response = await fetch(`${API_URL}/tickets/search/advanced?${params}`);
    const data = await response.json();
    setTickets(data.tickets || []);
    setIsLoading(false);
  }, [statusFilter, priorityFilter, categoryFilter, assigneeFilter]);

  const fetchStats = useCallback(async () => {
    const response = await fetch(`${API_URL}/tickets/stats/summary`);
    const data = await response.json();
    setStats(data);
  }, []);

  const fetchAgents = useCallback(async () => {
    const response = await fetch(`${API_URL}/tickets/agents`);
    const data = await response.json();
    setAgents(data.agents || []);
  }, []);

  useEffect(() => {
    fetchTickets();
    fetchStats();
    fetchAgents();
  }, [fetchTickets, fetchStats, fetchAgents]);

  useEffect(() => {
    if (createdTicket && selectedTicket?.id === createdTicket.id) {
      const ticketElement = document.getElementById(`ticket-${createdTicket.id}`);
      if (ticketElement) {
        ticketElement.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    }
  }, [createdTicket, selectedTicket]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleString("th-TH", {
      year: "numeric",
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const formatRelativeTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMins / 60);
    const diffDays = Math.floor(diffHours / 24);

    if (diffMins < 60) return `${diffMins} นาทีที่แล้ว`;
    if (diffHours < 24) return `${diffHours} ชั่วโมงที่แล้ว`;
    return `${diffDays} วันที่แล้ว`;
  };

  const handleCreateTicket = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsCreating(true);
    
    const formData = new FormData(e.currentTarget);
    
    const response = await fetch(`${API_URL}/tickets`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        subject: formData.get("subject"),
        description: formData.get("description"),
        priority: formData.get("priority"),
        requester_name: formData.get("requester_name"),
        requester_email: formData.get("requester_email"),
      }),
    });

    if (response.ok) {
      const data = await response.json();
      const newTicket = data.ticket;
      
      setShowCreateModal(false);
      setCreatedTicket(newTicket);
      setShowSuccessNotification(true);
      
      await fetchTickets();
      await fetchStats();
      
      setSelectedTicket(newTicket);
      
      setTimeout(() => {
        setShowSuccessNotification(false);
      }, 5000);
    }
    setIsCreating(false);
  };

  const updateTicketStatus = async (ticketId: number, newStatus: string) => {
    const response = await fetch(`${API_URL}/tickets/${ticketId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status: newStatus }),
    });

    if (response.ok) {
      fetchTickets();
      fetchStats();
      if (selectedTicket?.id === ticketId) {
        const data = await response.json();
        setSelectedTicket(data.ticket);
      }
    }
  };

  const assignTicket = async (ticketId: number, assigneeId: string) => {
    const response = await fetch(`${API_URL}/tickets/${ticketId}/assign`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ assignee_id: assigneeId }),
    });

    if (response.ok) {
      const data = await response.json();
      setSelectedTicket(data.ticket);
      await fetchTickets();
    }
  };

  const toggleTicketSelection = (ticketId: number) => {
    const newSelection = new Set(selectedTickets);
    if (newSelection.has(ticketId)) {
      newSelection.delete(ticketId);
    } else {
      newSelection.add(ticketId);
    }
    setSelectedTickets(newSelection);
  };

  const handleBulkUpdate = async (updates: any) => {
    const response = await fetch(`${API_URL}/tickets/bulk/update`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticket_ids: Array.from(selectedTickets),
        ...updates,
      }),
    });

    if (response.ok) {
      setSelectedTickets(new Set());
      setShowBulkActions(false);
      await fetchTickets();
      await fetchStats();
    }
  };

  const exportToCSV = async () => {
    const params = new URLSearchParams();
    if (statusFilter !== "all") params.append("status", statusFilter);
    if (priorityFilter !== "all") params.append("priority", priorityFilter);
    if (categoryFilter !== "all") params.append("category", categoryFilter);
    
    window.open(`${API_URL}/tickets/export/csv?${params}`, "_blank");
  };

  const isSLABreached = (ticket: Ticket) => {
    return ticket.sla_breach?.resolution_breached;
  };

  const filteredAndSortedTickets = useMemo(() => {
    let filtered = tickets;

    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase();
      filtered = filtered.filter((ticket) =>
        ticket.subject.toLowerCase().includes(query) ||
        ticket.description.toLowerCase().includes(query) ||
        ticket.requester_name.toLowerCase().includes(query) ||
        ticket.requester_email.toLowerCase().includes(query) ||
        ticket.id.toString().includes(query) ||
        ticket.tags.some(tag => tag.toLowerCase().includes(query))
      );
    }

    const sorted = [...filtered].sort((a, b) => {
      let comparison = 0;

      switch (sortBy) {
        case "created_at":
          comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
          break;
        case "updated_at":
          comparison = new Date(a.updated_at).getTime() - new Date(b.updated_at).getTime();
          break;
        case "priority":
          const priorityOrder = { urgent: 4, high: 3, normal: 2, low: 1 };
          comparison = priorityOrder[a.priority] - priorityOrder[b.priority];
          break;
        case "status":
          const statusOrder = { new: 1, open: 2, pending: 3, solved: 4, closed: 5 };
          comparison = statusOrder[a.status] - statusOrder[b.status];
          break;
      }

      return sortOrder === "asc" ? comparison : -comparison;
    });

    return sorted;
  }, [tickets, searchQuery, sortBy, sortOrder]);

  useEffect(() => {
    const handleKeyPress = (e: KeyboardEvent) => {
      if (e.ctrlKey || e.metaKey) {
        if (e.key === "k") {
          e.preventDefault();
          document.getElementById("search-input")?.focus();
        } else if (e.key === "n") {
          e.preventDefault();
          setShowCreateModal(true);
        } else if (e.key === "r") {
          e.preventDefault();
          fetchTickets();
          fetchStats();
        }
      }

      if (e.key === "Escape") {
        setShowCreateModal(false);
        setShowHistoryModal(false);
        setShowQuickActions(false);
        setSelectedTicket(null);
      }

      if (!showCreateModal && !showHistoryModal && filteredAndSortedTickets.length > 0) {
        const currentIndex = filteredAndSortedTickets.findIndex(t => t.id === selectedTicket?.id);
        if (e.key === "ArrowDown" && currentIndex < filteredAndSortedTickets.length - 1) {
          e.preventDefault();
          const nextTicket = filteredAndSortedTickets[currentIndex + 1];
          setSelectedTicket(nextTicket);
          document.getElementById(`ticket-${nextTicket.id}`)?.scrollIntoView({ behavior: "smooth", block: "nearest" });
        } else if (e.key === "ArrowUp" && currentIndex > 0) {
          e.preventDefault();
          const prevTicket = filteredAndSortedTickets[currentIndex - 1];
          setSelectedTicket(prevTicket);
          document.getElementById(`ticket-${prevTicket.id}`)?.scrollIntoView({ behavior: "smooth", block: "nearest" });
        }
      }
    };

    window.addEventListener("keydown", handleKeyPress);
    return () => window.removeEventListener("keydown", handleKeyPress);
  }, [selectedTicket, filteredAndSortedTickets, showCreateModal, showHistoryModal, fetchTickets, fetchStats]);

  const getSLATimeRemaining = (ticket: Ticket) => {
    const now = new Date();
    const dueDate = new Date(ticket.sla_resolution_due);
    const diffMs = dueDate.getTime() - now.getTime();
    const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
    const diffMins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));

    if (diffMs < 0) {
      return { text: "เกินกำหนด", urgent: true };
    } else if (diffHours < 2) {
      return { text: `${diffHours}ช ${diffMins}น`, urgent: true };
    } else if (diffHours < 24) {
      return { text: `${diffHours} ชั่วโมง`, urgent: false };
    } else {
      const diffDays = Math.floor(diffHours / 24);
      return { text: `${diffDays} วัน`, urgent: false };
    }
  };

  const clearFilters = () => {
    setStatusFilter("all");
    setPriorityFilter("all");
    setCategoryFilter("all");
    setAssigneeFilter("all");
    setSearchQuery("");
  };

  const hasActiveFilters = statusFilter !== "all" || priorityFilter !== "all" || 
    categoryFilter !== "all" || assigneeFilter !== "all" || searchQuery.trim() !== "";

  return (
    <div className="flex h-screen w-full bg-gradient-to-br from-typhoon-dark via-typhoon-darker to-black">
      <div className="flex flex-1 flex-col">
        {/* Header */}
        <header className="border-b border-rhythm bg-typhoon-darker/90 backdrop-blur-md shadow-sm">
          <div className="flex items-center justify-between px-6 py-4">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-gradient-to-br from-typhoon-primary to-lavender text-white shadow-lg ring-2 ring-lavender/20">
                <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">
                  ระบบจัดการ Ticket
                </h1>
                <p className="text-xs text-gray-400">
                  ดูและจัดการคำขอสนับสนุน
                </p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => {
                  fetchTickets();
                  fetchStats();
                }}
                title="Refresh (Ctrl/⌘+R)"
                className="group flex items-center gap-2 rounded-xl border-2 border-rhythm px-3 py-2 text-sm font-medium text-white transition-all hover:border-lavender hover:bg-lavender/10"
              >
                <svg className="h-5 w-5 transition-transform group-hover:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
              </button>
              <button
                onClick={exportToCSV}
                className="group flex items-center gap-2 rounded-xl border-2 border-rhythm px-4 py-2 text-sm font-medium text-white transition-all hover:border-lavender hover:bg-lavender/10"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                </svg>
                <span className="hidden md:inline">Export CSV</span>
              </button>
              <button
                onClick={() => setShowCreateModal(true)}
                title="สร้าง Ticket (Ctrl/⌘+N)"
                className="group flex items-center gap-2 rounded-xl bg-gradient-to-br from-typhoon-primary to-lavender px-4 py-2 text-sm font-medium text-white shadow-lg transition-all hover:shadow-xl hover:scale-105 active:scale-95"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" />
                </svg>
                <span>สร้าง Ticket</span>
              </button>
            </div>
          </div>
        </header>

        <div className="flex flex-1 overflow-hidden">
          {/* Tickets List */}
          <div className="flex flex-1 flex-col border-r border-rhythm bg-typhoon-darker/50">
            {/* Stats Bar */}
            {stats && (
              <div className="border-b border-rhythm bg-typhoon-darker/90 p-4">
                <div className="grid grid-cols-5 gap-3">
                  <div className="rounded-lg bg-gradient-to-br from-typhoon-primary/30 to-lavender/20 p-3 border border-lavender/20">
                    <div className="text-xs text-gray-400">Total</div>
                    <div className="text-2xl font-bold text-lavender">{stats.total}</div>
                  </div>
                  <div className="rounded-lg bg-gradient-to-br from-kobi/20 to-kobi/10 p-3 border border-kobi/20">
                    <div className="text-xs text-gray-400">Open</div>
                    <div className="text-2xl font-bold text-kobi">{stats.by_status.open || 0}</div>
                  </div>
                  <div className="rounded-lg bg-gradient-to-br from-desert/20 to-desert/10 p-3 border border-desert/20">
                    <div className="text-xs text-gray-400">Pending</div>
                    <div className="text-2xl font-bold text-desert">{stats.by_status.pending || 0}</div>
                  </div>
                  <div className="rounded-lg bg-gradient-to-br from-green-500/20 to-green-600/10 p-3 border border-green-500/20">
                    <div className="text-xs text-gray-400">Solved</div>
                    <div className="text-2xl font-bold text-green-400">{stats.by_status.solved || 0}</div>
                  </div>
                  <div className="rounded-lg bg-gradient-to-br from-cerulean/20 to-cerulean/10 p-3 border border-cerulean/20">
                    <div className="text-xs text-gray-400">Urgent</div>
                    <div className="text-2xl font-bold text-cerulean">{stats.by_priority.urgent || 0}</div>
                  </div>
                </div>
              </div>
            )}

            {/* Search & Filter Bar */}
            <div className="border-b border-rhythm bg-typhoon-darker/90 p-4 space-y-3">
              {/* Search Bar */}
              <div className="relative">
                <input
                  id="search-input"
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="ค้นหา ticket (Ctrl/⌘+K)"
                  className="w-full rounded-lg border-2 border-rhythm bg-typhoon-dark px-10 py-2.5 text-sm text-white placeholder:text-gray-400 focus:border-typhoon-primary focus:outline-none"
                />
                <svg className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
                {searchQuery && (
                  <button
                    onClick={() => setSearchQuery("")}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                  >
                    <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                )}
              </div>

              {/* Sort & Filters */}
              <div className="flex items-center gap-2 flex-wrap">
                <div className="flex items-center gap-2 bg-typhoon-dark rounded-lg px-3 py-1.5 border border-rhythm">
                  <svg className="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h6m4 0l4-4m0 0l4 4m-4-4v12" />
                  </svg>
                  <select
                    value={sortBy}
                    onChange={(e) => setSortBy(e.target.value as any)}
                    className="bg-transparent text-xs text-white focus:outline-none pr-6"
                  >
                    <option value="created_at">สร้างล่าสุด</option>
                    <option value="updated_at">อัปเดตล่าสุด</option>
                    <option value="priority">ความสำคัญ</option>
                    <option value="status">สถานะ</option>
                  </select>
                  <button
                    onClick={() => setSortOrder(sortOrder === "asc" ? "desc" : "asc")}
                    className="text-gray-400 hover:text-white transition-transform hover:scale-110"
                  >
                    {sortOrder === "asc" ? "↑" : "↓"}
                  </button>
                </div>

                <select
                  value={statusFilter}
                  onChange={(e) => setStatusFilter(e.target.value)}
                  className="rounded-lg border border-rhythm bg-typhoon-dark px-3 py-1.5 text-xs text-white focus:border-typhoon-primary focus:outline-none"
                >
                  <option value="all">สถานะ: ทั้งหมด</option>
                  <option value="new">ใหม่</option>
                  <option value="open">เปิด</option>
                  <option value="pending">รอดำเนินการ</option>
                  <option value="solved">แก้ไขแล้ว</option>
                  <option value="closed">ปิด</option>
                </select>

                <select
                  value={priorityFilter}
                  onChange={(e) => setPriorityFilter(e.target.value)}
                  className="rounded-lg border border-rhythm bg-typhoon-dark px-3 py-1.5 text-xs text-white focus:border-typhoon-primary focus:outline-none"
                >
                  <option value="all">ความสำคัญ: ทั้งหมด</option>
                  <option value="low">ต่ำ</option>
                  <option value="normal">ปกติ</option>
                  <option value="high">สูง</option>
                  <option value="urgent">ด่วน</option>
                </select>

                <select
                  value={categoryFilter}
                  onChange={(e) => setCategoryFilter(e.target.value)}
                  className="rounded-lg border border-rhythm bg-typhoon-dark px-3 py-1.5 text-xs text-white focus:border-typhoon-primary focus:outline-none"
                >
                  <option value="all">หมวดหมู่: ทั้งหมด</option>
                  {Object.entries(CATEGORY_LABELS).map(([key, label]) => (
                    <option key={key} value={key}>{label}</option>
                  ))}
                </select>

                <select
                  value={assigneeFilter}
                  onChange={(e) => setAssigneeFilter(e.target.value)}
                  className="rounded-lg border border-rhythm bg-typhoon-dark px-3 py-1.5 text-xs text-white focus:border-typhoon-primary focus:outline-none"
                >
                  <option value="all">ผู้รับผิดชอบ: ทั้งหมด</option>
                  <option value="">ยังไม่ได้มอบหมาย</option>
                  {agents.map((agent) => (
                    <option key={agent.id} value={agent.id}>{agent.name}</option>
                  ))}
                </select>

                {hasActiveFilters && (
                  <button
                    onClick={clearFilters}
                    className="text-xs text-gray-400 hover:text-white flex items-center gap-1 px-2 py-1 rounded hover:bg-rhythm transition-colors"
                  >
                    <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                    ล้างฟิลเตอร์
                  </button>
                )}
              </div>

              {/* Result Count */}
              <div className="flex items-center justify-between text-xs text-gray-400">
                <span>
                  แสดง {filteredAndSortedTickets.length} จาก {tickets.length} รายการ
                </span>
                {selectedTickets.size > 0 && (
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-gray-300">เลือก {selectedTickets.size} รายการ</span>
                    <button
                      onClick={() => setShowBulkActions(!showBulkActions)}
                      className="rounded-lg bg-lavender px-3 py-1 text-xs font-medium text-white hover:bg-lavender/80"
                    >
                      การดำเนินการแบบกลุ่ม
                    </button>
                    <button
                      onClick={() => setSelectedTickets(new Set())}
                      className="text-xs text-gray-400 hover:text-gray-200"
                    >
                      ยกเลิก
                    </button>
                  </div>
                )}
              </div>
            </div>

            {/* Bulk Actions */}
            {showBulkActions && selectedTickets.size > 0 && (
              <div className="border-b border-rhythm bg-lavender/10 p-4">
                <div className="flex gap-2">
                  <button
                    onClick={() => handleBulkUpdate({ status: "open" })}
                    className="rounded-lg bg-yellow-600 px-3 py-1 text-xs font-medium text-white hover:bg-yellow-700"
                  >
                    เปิด
                  </button>
                  <button
                    onClick={() => handleBulkUpdate({ status: "pending" })}
                    className="rounded-lg bg-orange-600 px-3 py-1 text-xs font-medium text-white hover:bg-orange-700"
                  >
                    รอดำเนินการ
                  </button>
                  <button
                    onClick={() => handleBulkUpdate({ status: "solved" })}
                    className="rounded-lg bg-green-600 px-3 py-1 text-xs font-medium text-white hover:bg-green-700"
                  >
                    แก้ไขแล้ว
                  </button>
                  <button
                    onClick={() => handleBulkUpdate({ priority: "urgent" })}
                    className="rounded-lg bg-red-600 px-3 py-1 text-xs font-medium text-white hover:bg-red-700"
                  >
                    ตั้งเป็นด่วน
                  </button>
                </div>
              </div>
            )}

            {/* Tickets List */}
            <div className="flex-1 overflow-y-auto p-4">
              {isLoading ? (
                <div className="flex h-full items-center justify-center">
                  <div className="flex flex-col items-center gap-3">
                    <div className="h-12 w-12 animate-spin rounded-full border-4 border-rhythm border-t-lavender"></div>
                    <div className="text-gray-400">กำลังโหลด...</div>
                  </div>
                </div>
              ) : filteredAndSortedTickets.length === 0 ? (
                <div className="flex h-full items-center justify-center">
                  <div className="text-center text-gray-400">
                    <svg className="mx-auto mb-2 h-12 w-12 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                    </svg>
                    <p className="text-lg font-semibold mb-1">ไม่พบ ticket</p>
                    {hasActiveFilters ? (
                      <p className="text-sm">ลองปรับฟิลเตอร์หรือคำค้นหาใหม่</p>
                    ) : (
                      <p className="text-sm">ยังไม่มี ticket ในระบบ</p>
                    )}
                  </div>
                </div>
              ) : (
                <div className="space-y-2">
                  {filteredAndSortedTickets.map((ticket) => {
                    const slaTime = getSLATimeRemaining(ticket);
                    return (
                    <div
                      key={ticket.id}
                      id={`ticket-${ticket.id}`}
                      onClick={() => setSelectedTicket(ticket)}
                      className={`cursor-pointer rounded-lg border-2 bg-typhoon-dark/80 p-4 shadow-sm transition-all hover:shadow-md ${
                        selectedTicket?.id === ticket.id
                          ? "border-typhoon-primary ring-2 ring-lavender/30"
                          : "border-rhythm"
                      } ${
                        createdTicket?.id === ticket.id
                          ? "animate-in fade-in slide-in-from-bottom-4 duration-500 ring-4 ring-green-400/30"
                          : ""
                      }`}
                    >
                      <div className="mb-2 flex items-start justify-between gap-2">
                        <div className="flex items-start gap-2 flex-1">
                          <input
                            type="checkbox"
                            checked={selectedTickets.has(ticket.id)}
                            onChange={(e) => {
                              e.stopPropagation();
                              toggleTicketSelection(ticket.id);
                            }}
                            className="mt-1 h-4 w-4 rounded border-rhythm bg-typhoon-darker text-lavender focus:ring-lavender"
                          />
                          <div className="flex-1">
                            <div className="flex items-center gap-2 flex-wrap">
                              <span className="text-sm font-semibold text-gray-400">
                                #{ticket.id}
                              </span>
                              <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_COLORS[ticket.status]}`}>
                                {ticket.status}
                              </span>
                              <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${PRIORITY_COLORS[ticket.priority]}`}>
                                {ticket.priority}
                              </span>
                              {ticket.status !== "solved" && ticket.status !== "closed" && (
                                <span className={`rounded-full px-2 py-0.5 text-xs font-medium flex items-center gap-1 ${
                                  slaTime.urgent ? "bg-red-500/20 text-red-400 border border-red-500/30 animate-pulse" : "bg-green-500/20 text-green-400 border border-green-500/30"
                                }`}>
                                  <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                                  </svg>
                                  {slaTime.text}
                                </span>
                              )}
                              {ticket.category && ticket.category !== "other" && (
                                <span className="rounded-full bg-lavender/20 px-2 py-0.5 text-xs font-medium text-lavender border border-lavender/30">
                                  {CATEGORY_LABELS[ticket.category]}
                                </span>
                              )}
                            </div>
                            <h3 className="mt-1 font-semibold text-white">
                              {ticket.subject}
                            </h3>
                          </div>
                        </div>
                      </div>
                      <p className="mb-2 line-clamp-2 text-sm text-gray-300">
                        {ticket.description}
                      </p>
                      <div className="flex items-center gap-3 text-xs text-gray-400">
                        <div className="flex items-center gap-1">
                          <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                          <span>{ticket.requester_name}</span>
                        </div>
                        {ticket.assignee_name && (
                          <div className="flex items-center gap-1 text-lavender">
                            <svg className="h-3 w-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                            </svg>
                            <span>{ticket.assignee_name}</span>
                          </div>
                        )}
                        <span className="ml-auto">{formatRelativeTime(ticket.created_at)}</span>
                      </div>
                      {ticket.tags && ticket.tags.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-1">
                          {ticket.tags.slice(0, 3).map((tag) => (
                            <span key={tag} className="rounded bg-rhythm px-2 py-0.5 text-xs text-gray-300">
                              #{tag}
                            </span>
                          ))}
                          {ticket.tags.length > 3 && (
                            <span className="rounded bg-rhythm px-2 py-0.5 text-xs text-gray-300">
                              +{ticket.tags.length - 3}
                            </span>
                          )}
                        </div>
                      )}
                    </div>
                  );
                  })}
                </div>
              )}
            </div>
          </div>

          {/* Ticket Detail Panel */}
          <div className="flex w-1/2 flex-col bg-typhoon-darker">
            {selectedTicket ? (
              <>
                <div className="border-b border-rhythm bg-typhoon-dark p-6">
                  <div className="mb-4 flex items-start justify-between">
                    <div className="flex-1">
                      <div className="mb-2 flex items-center gap-2 flex-wrap">
                        <span className="text-lg font-semibold text-gray-400">
                          Ticket #{selectedTicket.id}
                        </span>
                        <span className={`rounded-full px-3 py-1 text-sm font-medium ${STATUS_COLORS[selectedTicket.status]}`}>
                          {selectedTicket.status}
                        </span>
                        <span className={`rounded-full px-3 py-1 text-sm font-medium ${PRIORITY_COLORS[selectedTicket.priority]}`}>
                          {selectedTicket.priority}
                        </span>
                        {selectedTicket.status !== "solved" && selectedTicket.status !== "closed" && (() => {
                          const slaTime = getSLATimeRemaining(selectedTicket);
                          return (
                            <span className={`rounded-full px-3 py-1 text-sm font-medium flex items-center gap-1 ${
                              slaTime.urgent ? "bg-red-500/20 text-red-400 border border-red-500/30 animate-pulse" : "bg-green-500/20 text-green-400 border border-green-500/30"
                            }`}>
                              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                              </svg>
                              SLA: {slaTime.text}
                            </span>
                          );
                        })()}
                      </div>
                      <h2 className="text-2xl font-bold text-white">
                        {selectedTicket.subject}
                      </h2>
                    </div>
                    <button
                      onClick={() => setSelectedTicket(null)}
                      title="Close (ESC)"
                      className="rounded-lg p-2 text-gray-400 transition-colors hover:bg-rhythm hover:text-gray-200"
                    >
                      <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                      </svg>
                    </button>
                  </div>

                  <div className="mb-4 grid grid-cols-2 gap-4 text-sm">
                    <div>
                      <div className="text-gray-400">ผู้ส่งคำขอ</div>
                      <div className="font-medium text-white">
                        {selectedTicket.requester_name}
                      </div>
                      <div className="text-gray-300">{selectedTicket.requester_email}</div>
                    </div>
                    <div>
                      <div className="text-gray-400">ผู้รับผิดชอบ</div>
                      <select
                        value={selectedTicket.assignee_id || ""}
                        onChange={(e) => assignTicket(selectedTicket.id, e.target.value)}
                        className="mt-1 w-full rounded-lg border-2 border-rhythm bg-typhoon-darker px-3 py-1 text-white focus:border-typhoon-primary focus:outline-none"
                      >
                        <option value="">ยังไม่ได้มอบหมาย</option>
                        {agents.map((agent) => (
                          <option key={agent.id} value={agent.id}>{agent.name}</option>
                        ))}
                      </select>
                    </div>
                    <div>
                      <div className="text-gray-400">หมวดหมู่</div>
                      <div className="font-medium text-white">
                        {CATEGORY_LABELS[selectedTicket.category] || "ไม่ระบุ"}
                      </div>
                    </div>
                    <div>
                      <div className="text-gray-400">สร้างเมื่อ</div>
                      <div className="font-medium text-white">
                        {formatDate(selectedTicket.created_at)}
                      </div>
                    </div>
                  </div>

                  {selectedTicket.tags && selectedTicket.tags.length > 0 && (
                    <div className="mb-4">
                      <div className="text-sm text-gray-400 mb-1">Tags</div>
                      <div className="flex flex-wrap gap-1">
                        {selectedTicket.tags.map((tag) => (
                          <span key={tag} className="rounded-full bg-lavender/20 px-3 py-1 text-xs font-medium text-lavender border border-lavender/30">
                            #{tag}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="flex gap-2 flex-wrap">
                    {["new", "open", "pending", "solved", "closed"].map((status) => (
                      <button
                        key={status}
                        onClick={() => updateTicketStatus(selectedTicket.id, status)}
                        disabled={selectedTicket.status === status}
                        className={`rounded-lg px-3 py-1 text-sm font-medium transition-all ${
                          selectedTicket.status === status
                            ? "cursor-not-allowed opacity-50"
                            : "hover:scale-105"
                        } ${STATUS_COLORS[status as keyof typeof STATUS_COLORS]}`}
                      >
                        {status}
                      </button>
                    ))}
                    <button
                      onClick={() => setShowHistoryModal(true)}
                      className="rounded-lg border-2 border-rhythm px-3 py-1 text-sm font-medium text-gray-300 hover:border-lavender hover:text-lavender"
                    >
                      📜 ประวัติ
                    </button>
                  </div>
                </div>

                <div className="flex-1 overflow-y-auto p-6">
                  <div className="mb-6">
                    <h3 className="mb-2 font-semibold text-white">รายละเอียด</h3>
                    <p className="whitespace-pre-wrap text-gray-200">
                      {selectedTicket.description}
                    </p>
                  </div>

                  {selectedTicket.comments.length > 0 && (
                    <div>
                      <h3 className="mb-3 font-semibold text-white">
                        ความคิดเห็น ({selectedTicket.comments.length})
                      </h3>
                      <div className="space-y-3">
                        {selectedTicket.comments.map((comment, idx) => (
                          <div
                            key={idx}
                            className="rounded-lg border border-rhythm bg-typhoon-dark/50 p-4"
                          >
                            <div className="mb-2 flex items-center justify-between">
                              <span className="font-medium text-white">
                                {comment.author}
                              </span>
                              <span className="text-xs text-gray-400">
                                {formatDate(comment.created_at)}
                              </span>
                            </div>
                            <p className="text-sm text-gray-200">{comment.body}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div className="flex h-full items-center justify-center">
                <div className="text-center text-gray-400">
                  <svg className="mx-auto mb-2 h-16 w-16 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                  </svg>
                  <p>เลือก ticket เพื่อดูรายละเอียด</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Create Ticket Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
          <div className="w-full max-w-lg rounded-2xl bg-typhoon-darker border-2 border-rhythm p-6 shadow-2xl">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-bold text-white">สร้าง Ticket ใหม่</h2>
              <button
                onClick={() => setShowCreateModal(false)}
                className="rounded-lg p-2 text-gray-400 transition-colors hover:bg-rhythm hover:text-gray-200"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <form onSubmit={handleCreateTicket} className="space-y-4">
              <div>
                <label className="mb-1 block text-sm font-medium text-gray-300">
                  หัวข้อ
                </label>
                <input
                  type="text"
                  name="subject"
                  required
                  className="w-full rounded-lg border-2 border-rhythm bg-typhoon-dark px-4 py-2 text-white focus:border-typhoon-primary focus:outline-none"
                />
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-gray-300">
                  รายละเอียด
                </label>
                <textarea
                  name="description"
                  required
                  rows={4}
                  className="w-full rounded-lg border-2 border-rhythm bg-typhoon-dark px-4 py-2 text-white focus:border-typhoon-primary focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-300">
                    ชื่อ
                  </label>
                  <input
                    type="text"
                    name="requester_name"
                    required
                    defaultValue={user ? `${user.full_name_th} (${user.nickname})` : "User"}
                    className="w-full rounded-lg border-2 border-rhythm bg-typhoon-dark px-4 py-2 text-white focus:border-typhoon-primary focus:outline-none"
                  />
                </div>

                <div>
                  <label className="mb-1 block text-sm font-medium text-gray-300">
                    อีเมล
                  </label>
                  <input
                    type="email"
                    name="requester_email"
                    required
                    defaultValue={user?.email || "user@company.com"}
                    className="w-full rounded-lg border-2 border-rhythm bg-typhoon-dark px-4 py-2 text-white focus:border-typhoon-primary focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="mb-1 block text-sm font-medium text-gray-300">
                  ความสำคัญ
                </label>
                <select
                  name="priority"
                  defaultValue="normal"
                  className="w-full rounded-lg border-2 border-rhythm bg-typhoon-dark px-4 py-2 text-white focus:border-typhoon-primary focus:outline-none"
                >
                  <option value="low">ต่ำ</option>
                  <option value="normal">ปกติ</option>
                  <option value="high">สูง</option>
                  <option value="urgent">ด่วน</option>
                </select>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  disabled={isCreating}
                  className="flex-1 rounded-xl border-2 border-rhythm px-4 py-2 font-medium text-gray-300 transition-colors hover:bg-rhythm disabled:cursor-not-allowed disabled:opacity-50"
                >
                  ยกเลิก
                </button>
                <button
                  type="submit"
                  disabled={isCreating}
                  className="flex-1 rounded-xl bg-gradient-to-br from-typhoon-primary to-lavender px-4 py-2 font-medium text-white shadow-lg transition-all hover:shadow-xl hover:scale-105 disabled:cursor-not-allowed disabled:opacity-50 disabled:hover:scale-100 flex items-center justify-center gap-2"
                >
                  {isCreating ? (
                    <>
                      <svg
                        className="h-5 w-5 animate-spin"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <circle
                          className="opacity-25"
                          cx="12"
                          cy="12"
                          r="10"
                          stroke="currentColor"
                          strokeWidth="4"
                        ></circle>
                        <path
                          className="opacity-75"
                          fill="currentColor"
                          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                        ></path>
                      </svg>
                      <span>กำลังสร้าง...</span>
                    </>
                  ) : (
                    "สร้าง Ticket"
                  )}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* History Modal */}
      {showHistoryModal && selectedTicket && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
          <div className="w-full max-w-2xl rounded-2xl bg-typhoon-darker border-2 border-rhythm p-6 shadow-2xl max-h-[80vh] overflow-y-auto">
            <div className="mb-4 flex items-center justify-between">
              <h2 className="text-xl font-bold text-white">ประวัติการเปลี่ยนแปลง</h2>
              <button
                onClick={() => setShowHistoryModal(false)}
                className="rounded-lg p-2 text-gray-400 transition-colors hover:bg-rhythm hover:text-gray-200"
              >
                <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            <div className="space-y-3">
              {selectedTicket.history.map((entry, idx) => (
                <div key={idx} className="rounded-lg border border-rhythm bg-typhoon-dark/50 p-4">
                  <div className="mb-2 flex items-start justify-between">
                    <div>
                      <div className="font-medium text-white">{entry.action}</div>
                      <div className="text-sm text-gray-400">โดย {entry.actor}</div>
                    </div>
                    <div className="text-xs text-gray-400">
                      {formatDate(entry.timestamp)}
                    </div>
                  </div>
                  <div className="text-sm text-gray-300">
                    <pre className="whitespace-pre-wrap font-sans">
                      {JSON.stringify(entry.changes, null, 2)}
                    </pre>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Success Notification */}
      {showSuccessNotification && createdTicket && (
        <div className="fixed bottom-6 right-6 z-50 animate-in slide-in-from-bottom-4 fade-in duration-300">
          <div className="flex items-start gap-4 rounded-2xl border-2 border-green-400 bg-typhoon-darker p-6 shadow-2xl max-w-md">
            <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-gradient-to-br from-green-500 to-emerald-600 text-white shadow-lg">
              <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <div className="flex-1">
              <h3 className="text-lg font-bold text-white mb-1">
                🎉 สร้าง Ticket สำเร็จ!
              </h3>
              <p className="text-sm text-gray-300 mb-2">
                Ticket #{createdTicket.id} ถูกสร้างเรียบร้อยแล้ว
              </p>
              <div className="rounded-lg bg-typhoon-dark p-3 mb-3">
                <div className="flex items-start gap-2 mb-2">
                  <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${STATUS_COLORS[createdTicket.status]}`}>
                    {createdTicket.status}
                  </span>
                  <span className={`rounded-full px-2 py-0.5 text-xs font-medium ${PRIORITY_COLORS[createdTicket.priority]}`}>
                    {createdTicket.priority}
                  </span>
                </div>
                <p className="font-semibold text-white text-sm mb-1">
                  {createdTicket.subject}
                </p>
                <p className="text-xs text-gray-400">
                  ผู้ส่งคำขอ: {createdTicket.requester_name}
                </p>
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => setShowSuccessNotification(false)}
                  className="flex-1 rounded-lg bg-rhythm px-3 py-2 text-sm font-medium text-gray-200 transition-colors hover:bg-rhythm/80"
                >
                  ปิด
                </button>
                <button
                  onClick={() => {
                    setSelectedTicket(createdTicket);
                    setShowSuccessNotification(false);
                  }}
                  className="flex-1 rounded-lg bg-gradient-to-br from-typhoon-primary to-lavender px-3 py-2 text-sm font-medium text-white transition-all hover:shadow-lg hover:scale-105"
                >
                  ดูรายละเอียด
                </button>
              </div>
            </div>
            <button
              onClick={() => setShowSuccessNotification(false)}
              className="rounded-lg p-1 text-gray-400 transition-colors hover:bg-rhythm hover:text-gray-200"
            >
              <svg className="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
        </div>
      )}

      {/* Keyboard Shortcuts Help */}
      <div className="fixed bottom-4 left-4 bg-typhoon-darker/95 border border-rhythm rounded-lg px-4 py-2 text-xs text-gray-400 backdrop-blur-sm shadow-lg">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1">
            <kbd className="rounded bg-typhoon-dark px-1.5 py-0.5 font-mono border border-rhythm">⌘/Ctrl+K</kbd>
            <span>ค้นหา</span>
          </div>
          <div className="flex items-center gap-1">
            <kbd className="rounded bg-typhoon-dark px-1.5 py-0.5 font-mono border border-rhythm">⌘/Ctrl+N</kbd>
            <span>สร้าง</span>
          </div>
          <div className="flex items-center gap-1">
            <kbd className="rounded bg-typhoon-dark px-1.5 py-0.5 font-mono border border-rhythm">↑↓</kbd>
            <span>นำทาง</span>
          </div>
          <div className="flex items-center gap-1">
            <kbd className="rounded bg-typhoon-dark px-1.5 py-0.5 font-mono border border-rhythm">ESC</kbd>
            <span>ปิด</span>
          </div>
        </div>
      </div>
    </div>
  );
}
