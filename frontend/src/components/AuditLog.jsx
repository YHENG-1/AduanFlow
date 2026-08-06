import React, { useState, useMemo } from 'react';
import { IconSearch } from './Icons';

export default function AuditLog({ cases = [] }) {
  const [search, setSearch] = useState('');
  const [actorFilter, setActorFilter] = useState('All');

  // Build audit timeline from live case data (auditLog) fetched from backend
  const allLogs = useMemo(
    () => cases.flatMap((c) => (c.auditLog || []).map((entry) => ({ ...entry, caseId: c.id }))),
    [cases]
  );

  const allActors = useMemo(
    () => ['All', ...new Set(allLogs.map((l) => l.actor))].sort(),
    [allLogs]
  );

  const filtered = allLogs.filter((l) => {
    const matchSearch = l.caseId.toLowerCase().includes(search.toLowerCase()) ||
      l.action.toLowerCase().includes(search.toLowerCase()) ||
      l.detail.toLowerCase().includes(search.toLowerCase());
    const matchActor = actorFilter === 'All' || l.actor === actorFilter;
    return matchSearch && matchActor;
  });

  return (
    <div className="space-y-6">
      {/* Page header */}
      <div>
        <h2 className="text-2xl font-bold text-slate-900">Audit Log</h2>
        <p className="text-sm text-slate-500 mt-0.5">Complete audit trail across all cases — {allLogs.length} events</p>
      </div>

      {/* Filter bar */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-card p-4">
        <div className="flex flex-wrap items-center gap-3">
          <div className="flex-1 min-w-[240px] relative">
            <IconSearch className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none" />
            <input
              type="text"
              placeholder="Search audit events..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-2 text-sm border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
            />
          </div>
          <select
            value={actorFilter}
            onChange={(e) => setActorFilter(e.target.value)}
            className="px-3 py-2 text-sm border border-slate-200 rounded-lg bg-white focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-colors"
          >
            {allActors.map((a) => (
              <option key={a} value={a}>{a === 'All' ? 'All Actors' : a}</option>
            ))}
          </select>
          <span className="text-xs text-slate-500 ml-auto">{filtered.length} events</span>
        </div>
      </div>

      {/* Timeline */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-card p-6">
        <div className="space-y-0">
          {filtered.map((entry, idx) => (
            <div key={idx} className="flex gap-3 pb-4 relative">
              {idx < filtered.length - 1 && <div className="absolute left-[5.5px] top-5 bottom-0 w-px bg-slate-100" />}
              <div className="w-3 h-3 rounded-full bg-blue-500 flex-shrink-0 mt-1.5 ring-2 ring-blue-100" />
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-0.5 flex-wrap">
                  <span className="text-xs font-mono text-slate-500">{entry.time}</span>
                  <span className="text-xs font-medium text-blue-600">{entry.actor}</span>
                  <span className="text-xs font-mono text-slate-500">{entry.caseId}</span>
                </div>
                <p className="text-sm text-slate-700">{entry.action}</p>
                <p className="text-xs text-slate-500 mt-0.5">{entry.detail}</p>
              </div>
            </div>
          ))}
        </div>
        {filtered.length === 0 && (
          <div className="text-center py-12 text-slate-500">
            <p>No audit events match your filters</p>
          </div>
        )}
      </div>
    </div>
  );
}
