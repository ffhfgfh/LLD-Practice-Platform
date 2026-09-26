import React, { useState, useEffect } from 'react';
import { ClassDesign, ClassAttribute, ClassMethod, ClassRelationship } from '../../types';
import { Button } from '../common/Button';
import { Plus, Trash2, X, Sparkles, Layers, Wand2 } from 'lucide-react';

interface ClassEditorModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSave: (classDesign: ClassDesign) => void;
  initialData?: ClassDesign | null;
  existingClassNames?: string[];
}

export const ClassEditorModal: React.FC<ClassEditorModalProps> = ({
  isOpen,
  onClose,
  onSave,
  initialData,
  existingClassNames = [],
}) => {
  const [name, setName] = useState('');
  const [responsibility, setResponsibility] = useState('');
  const [isInterface, setIsInterface] = useState(false);
  const [isAbstract, setIsAbstract] = useState(false);
  const [interfacesImplemented, setInterfacesImplemented] = useState<string[]>([]);
  const [interfaceInput, setInterfaceInput] = useState('');

  const [attributes, setAttributes] = useState<ClassAttribute[]>([]);
  const [methods, setMethods] = useState<ClassMethod[]>([]);
  const [relationships, setRelationships] = useState<ClassRelationship[]>([]);

  useEffect(() => {
    if (initialData) {
      setName(initialData.name || '');
      setResponsibility(initialData.responsibility || '');
      setIsInterface(initialData.is_interface || false);
      setIsAbstract(initialData.is_abstract || false);
      setInterfacesImplemented(initialData.interfaces_implemented || []);
      setAttributes(initialData.attributes || []);
      setMethods(initialData.methods || []);
      setRelationships(initialData.relationships || []);
    } else {
      setName('');
      setResponsibility('');
      setIsInterface(false);
      setIsAbstract(false);
      setInterfacesImplemented([]);
      setAttributes([]);
      setMethods([]);
      setRelationships([]);
    }
  }, [initialData, isOpen]);

  if (!isOpen) return null;

  // Preset Template Applicator
  const applyPreset = (preset: 'strategy_interface' | 'singleton_controller' | 'factory' | 'abstract_entity') => {
    if (preset === 'strategy_interface') {
      setName('PaymentStrategy');
      setIsInterface(true);
      setIsAbstract(false);
      setResponsibility('Interface contract defining polymorphic payment calculation and processing algorithms.');
      setMethods([
        { name: 'processPayment', returnType: 'PaymentReceipt', params: 'double amount, Customer c', visibility: 'public' }
      ]);
    } else if (preset === 'singleton_controller') {
      setName('ParkingLotController');
      setIsInterface(false);
      setIsAbstract(false);
      setResponsibility('Central orchestrator coordinating entry gates, floor capacities, and hardware events.');
      setAttributes([
        { name: 'instance', type: 'ParkingLotController', visibility: 'private' },
        { name: 'floors', type: 'List<ParkingFloor>', visibility: 'private' }
      ]);
      setMethods([
        { name: 'getInstance', returnType: 'ParkingLotController', params: '', visibility: 'public' },
        { name: 'processEntry', returnType: 'Ticket', params: 'Vehicle v', visibility: 'public' }
      ]);
    } else if (preset === 'abstract_entity') {
      setName('Vehicle');
      setIsInterface(false);
      setIsAbstract(true);
      setResponsibility('Abstract base class encapsulating common vehicle identity and license dimensions.');
      setAttributes([
        { name: 'licensePlate', type: 'string', visibility: 'protected' },
        { name: 'vehicleType', type: 'VehicleType', visibility: 'protected' }
      ]);
      setMethods([
        { name: 'getVehicleType', returnType: 'VehicleType', params: '', visibility: 'public' }
      ]);
    } else if (preset === 'factory') {
      setName('VehicleFactory');
      setIsInterface(false);
      setIsAbstract(false);
      setResponsibility('Factory responsible for instantiating concrete Vehicle subclasses based on type.');
      setMethods([
        { name: 'createVehicle', returnType: 'Vehicle', params: 'VehicleType type, string plate', visibility: 'public' }
      ]);
    }
  };

  // Attribute Handlers
  const addAttribute = () => {
    setAttributes([...attributes, { name: '', type: 'string', visibility: 'private' }]);
  };
  const updateAttribute = (index: number, field: keyof ClassAttribute, val: string) => {
    const next = [...attributes];
    next[index] = { ...next[index], [field]: val };
    setAttributes(next);
  };
  const removeAttribute = (index: number) => {
    setAttributes(attributes.filter((_, i) => i !== index));
  };

  // Method Handlers
  const addMethod = () => {
    setMethods([...methods, { name: '', returnType: 'void', params: '', visibility: 'public' }]);
  };
  const updateMethod = (index: number, field: keyof ClassMethod, val: string) => {
    const next = [...methods];
    next[index] = { ...next[index], [field]: val };
    setMethods(next);
  };
  const removeMethod = (index: number) => {
    setMethods(methods.filter((_, i) => i !== index));
  };

  // Relationship Handlers
  const addRelationship = () => {
    setRelationships([...relationships, { target: '', type: 'ASSOCIATION', multiplicity: '1' }]);
  };
  const updateRelationship = (index: number, field: keyof ClassRelationship, val: string) => {
    const next = [...relationships];
    next[index] = { ...next[index], [field]: val };
    setRelationships(next);
  };
  const removeRelationship = (index: number) => {
    setRelationships(relationships.filter((_, i) => i !== index));
  };

  // Interface Implemented Handlers
  const addInterfaceImplemented = () => {
    if (interfaceInput.trim() && !interfacesImplemented.includes(interfaceInput.trim())) {
      setInterfacesImplemented([...interfacesImplemented, interfaceInput.trim()]);
      setInterfaceInput('');
    }
  };
  const removeInterfaceImplemented = (item: string) => {
    setInterfacesImplemented(interfacesImplemented.filter((i) => i !== item));
  };

  const handleSave = () => {
    if (!name.trim()) {
      alert('Class name is required.');
      return;
    }
    if (!responsibility.trim() || responsibility.trim().length < 8) {
      alert('Please provide a clear Single Responsibility explanation (at least 8 characters).');
      return;
    }

    onSave({
      id: initialData?.id,
      name: name.trim(),
      responsibility: responsibility.trim(),
      is_interface: isInterface,
      is_abstract: isAbstract,
      interfaces_implemented: interfacesImplemented,
      attributes: attributes.filter((a) => a.name.trim()),
      methods: methods.filter((m) => m.name.trim()),
      relationships: relationships.filter((r) => r.target.trim()),
    });
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/80 backdrop-blur-sm p-4 overflow-y-auto">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl w-full max-w-3xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div className="flex items-center gap-2">
            <Layers className="h-5 w-5 text-indigo-400" />
            <h3 className="text-lg font-bold text-white">
              {initialData ? 'Edit Class / Entity' : 'Add Class / Entity'}
            </h3>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1">
          {/* Preset Patterns for quick start */}
          {!initialData && (
            <div className="p-3 rounded-xl bg-indigo-950/30 border border-indigo-500/20">
              <div className="text-xs font-semibold uppercase tracking-wider text-indigo-300 flex items-center gap-1.5 mb-2">
                <Wand2 className="h-3.5 w-3.5 text-indigo-400" />
                Quick Entity Presets
              </div>
              <div className="flex flex-wrap gap-2">
                <button
                  type="button"
                  onClick={() => applyPreset('strategy_interface')}
                  className="text-xs px-2.5 py-1 rounded bg-slate-800 text-indigo-300 hover:bg-indigo-600 hover:text-white transition-colors"
                >
                  + Strategy Interface
                </button>
                <button
                  type="button"
                  onClick={() => applyPreset('singleton_controller')}
                  className="text-xs px-2.5 py-1 rounded bg-slate-800 text-indigo-300 hover:bg-indigo-600 hover:text-white transition-colors"
                >
                  + Orchestrator / Controller
                </button>
                <button
                  type="button"
                  onClick={() => applyPreset('abstract_entity')}
                  className="text-xs px-2.5 py-1 rounded bg-slate-800 text-indigo-300 hover:bg-indigo-600 hover:text-white transition-colors"
                >
                  + Abstract Base Class
                </button>
                <button
                  type="button"
                  onClick={() => applyPreset('factory')}
                  className="text-xs px-2.5 py-1 rounded bg-slate-800 text-indigo-300 hover:bg-indigo-600 hover:text-white transition-colors"
                >
                  + Factory Class
                </button>
              </div>
            </div>
          )}

          {/* Name & Type */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                Class / Entity Name <span className="text-rose-400">*</span>
              </label>
              <input
                type="text"
                placeholder="e.g. ParkingLot, SpotAllocationStrategy"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                Entity Modifiers
              </label>
              <div className="flex items-center gap-4 mt-2">
                <label className="inline-flex items-center gap-2 text-sm text-slate-300 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isInterface}
                    onChange={(e) => {
                      setIsInterface(e.target.checked);
                      if (e.target.checked) setIsAbstract(false);
                    }}
                    className="rounded bg-slate-950 border-slate-700 text-indigo-600 focus:ring-indigo-500"
                  />
                  <span>Is Interface</span>
                </label>

                <label className="inline-flex items-center gap-2 text-sm text-slate-300 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={isAbstract}
                    onChange={(e) => {
                      setIsAbstract(e.target.checked);
                      if (e.target.checked) setIsInterface(false);
                    }}
                    className="rounded bg-slate-950 border-slate-700 text-indigo-600 focus:ring-indigo-500"
                  />
                  <span>Is Abstract Class</span>
                </label>
              </div>
            </div>
          </div>

          {/* Single Responsibility */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
              Single Responsibility (SRP) <span className="text-rose-400">*</span>
            </label>
            <textarea
              rows={2}
              placeholder="What is the single reason for this class to change? e.g., Responsible for maintaining physical spot occupancy state."
              value={responsibility}
              onChange={(e) => setResponsibility(e.target.value)}
              className="w-full px-3.5 py-2 rounded-lg bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            />
          </div>

          {/* Implements Interfaces */}
          {!isInterface && (
            <div>
              <label className="block text-xs font-semibold uppercase tracking-wider text-slate-300 mb-1.5">
                Implemented Interfaces / Base Classes
              </label>
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="e.g. PaymentProcessor, AllocationStrategy"
                  value={interfaceInput}
                  onChange={(e) => setInterfaceInput(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addInterfaceImplemented())}
                  className="flex-1 px-3 py-1.5 rounded-lg bg-slate-950 border border-slate-700 text-white placeholder-slate-500 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
                <Button variant="secondary" size="sm" onClick={addInterfaceImplemented}>
                  Add
                </Button>
              </div>
              {interfacesImplemented.length > 0 && (
                <div className="flex flex-wrap gap-1.5 mt-2">
                  {interfacesImplemented.map((iface) => (
                    <span
                      key={iface}
                      className="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-indigo-500/15 text-indigo-300 border border-indigo-500/30 text-xs font-mono"
                    >
                      {iface}
                      <button
                        onClick={() => removeInterfaceImplemented(iface)}
                        className="hover:text-rose-400 ml-1"
                      >
                        &times;
                      </button>
                    </span>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Attributes Section */}
          <div className="border-t border-slate-800 pt-4">
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                Attributes ({attributes.length})
              </label>
              <Button variant="outline" size="sm" onClick={addAttribute} leftIcon={<Plus className="h-3 w-3" />}>
                Add Attribute
              </Button>
            </div>

            {attributes.length === 0 ? (
              <p className="text-xs text-slate-500 italic">No attributes added yet.</p>
            ) : (
              <div className="space-y-2">
                {attributes.map((attr, idx) => (
                  <div key={idx} className="flex items-center gap-2">
                    <select
                      value={attr.visibility}
                      onChange={(e) => updateAttribute(idx, 'visibility', e.target.value as any)}
                      className="px-2 py-1.5 rounded bg-slate-950 border border-slate-700 text-slate-300 text-xs font-mono"
                    >
                      <option value="private">- private</option>
                      <option value="public">+ public</option>
                      <option value="protected"># protected</option>
                    </select>

                    <input
                      type="text"
                      placeholder="name (e.g. spotNumber)"
                      value={attr.name}
                      onChange={(e) => updateAttribute(idx, 'name', e.target.value)}
                      className="flex-1 px-3 py-1.5 rounded bg-slate-950 border border-slate-700 text-white text-xs font-mono"
                    />

                    <input
                      type="text"
                      placeholder="type (e.g. int, SpotType)"
                      value={attr.type}
                      onChange={(e) => updateAttribute(idx, 'type', e.target.value)}
                      className="w-36 px-3 py-1.5 rounded bg-slate-950 border border-slate-700 text-slate-300 text-xs font-mono"
                    />

                    <button
                      onClick={() => removeAttribute(idx)}
                      className="text-slate-500 hover:text-rose-400 p-1"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Methods Section */}
          <div className="border-t border-slate-800 pt-4">
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                Methods & Operations ({methods.length})
              </label>
              <Button variant="outline" size="sm" onClick={addMethod} leftIcon={<Plus className="h-3 w-3" />}>
                Add Method
              </Button>
            </div>

            {methods.length === 0 ? (
              <p className="text-xs text-slate-500 italic">No methods added yet.</p>
            ) : (
              <div className="space-y-2">
                {methods.map((method, idx) => (
                  <div key={idx} className="flex items-center gap-2">
                    <select
                      value={method.visibility}
                      onChange={(e) => updateMethod(idx, 'visibility', e.target.value as any)}
                      className="px-2 py-1.5 rounded bg-slate-950 border border-slate-700 text-slate-300 text-xs font-mono"
                    >
                      <option value="public">+ public</option>
                      <option value="private">- private</option>
                      <option value="protected"># protected</option>
                    </select>

                    <input
                      type="text"
                      placeholder="methodName"
                      value={method.name}
                      onChange={(e) => updateMethod(idx, 'name', e.target.value)}
                      className="flex-1 px-3 py-1.5 rounded bg-slate-950 border border-slate-700 text-white text-xs font-mono"
                    />

                    <input
                      type="text"
                      placeholder="params (e.g. Vehicle v)"
                      value={method.params}
                      onChange={(e) => updateMethod(idx, 'params', e.target.value)}
                      className="w-44 px-3 py-1.5 rounded bg-slate-950 border border-slate-700 text-slate-300 text-xs font-mono"
                    />

                    <input
                      type="text"
                      placeholder="returnType"
                      value={method.returnType}
                      onChange={(e) => updateMethod(idx, 'returnType', e.target.value)}
                      className="w-28 px-3 py-1.5 rounded bg-slate-950 border border-slate-700 text-slate-300 text-xs font-mono"
                    />

                    <button
                      onClick={() => removeMethod(idx)}
                      className="text-slate-500 hover:text-rose-400 p-1"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Relationships Section */}
          <div className="border-t border-slate-800 pt-4">
            <div className="flex items-center justify-between mb-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-slate-300">
                Relationships to Other Classes ({relationships.length})
              </label>
              <Button variant="outline" size="sm" onClick={addRelationship} leftIcon={<Plus className="h-3 w-3" />}>
                Add Relationship
              </Button>
            </div>

            {relationships.length === 0 ? (
              <p className="text-xs text-slate-500 italic">No explicit relationships configured.</p>
            ) : (
              <div className="space-y-2">
                {relationships.map((rel, idx) => (
                  <div key={idx} className="flex items-center gap-2">
                    <select
                      value={rel.type}
                      onChange={(e) => updateRelationship(idx, 'type', e.target.value as any)}
                      className="px-2.5 py-1.5 rounded bg-slate-950 border border-slate-700 text-slate-300 text-xs font-mono"
                    >
                      <option value="ASSOCIATION">Association (uses/knows --&gt;)</option>
                      <option value="COMPOSITION">Composition (owns exclusively *--)</option>
                      <option value="AGGREGATION">Aggregation (has-a o--)</option>
                      <option value="INHERITANCE">Inheritance (is-a --|&gt;)</option>
                      <option value="IMPLEMENTATION">Implementation (implements ..|&gt;)</option>
                    </select>

                    <input
                      type="text"
                      placeholder="Target Class Name"
                      value={rel.target}
                      onChange={(e) => updateRelationship(idx, 'target', e.target.value)}
                      list="class-suggestions"
                      className="flex-1 px-3 py-1.5 rounded bg-slate-950 border border-slate-700 text-white text-xs font-mono"
                    />

                    <input
                      type="text"
                      placeholder="Multiplicity (1, 1..*, 0..1)"
                      value={rel.multiplicity}
                      onChange={(e) => updateRelationship(idx, 'multiplicity', e.target.value)}
                      className="w-32 px-3 py-1.5 rounded bg-slate-950 border border-slate-700 text-slate-300 text-xs font-mono"
                    />

                    <button
                      onClick={() => removeRelationship(idx)}
                      className="text-slate-500 hover:text-rose-400 p-1"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                ))}

                <datalist id="class-suggestions">
                  {existingClassNames.map((c) => (
                    <option key={c} value={c} />
                  ))}
                </datalist>
              </div>
            )}
          </div>
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-4 border-t border-slate-800 bg-slate-950/60 flex items-center justify-end gap-3">
          <Button variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleSave}>
            Save Class Design
          </Button>
        </div>
      </div>
    </div>
  );
};
