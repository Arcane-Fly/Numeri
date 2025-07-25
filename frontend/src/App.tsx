import { useState } from 'react';
import { FileText, Calculator, Home, Menu, X } from 'lucide-react';
import './index.css';
import { Dashboard } from './components/Dashboard';
import { FileUpload } from './components/FileUpload';
import { DocumentList } from './components/DocumentList';
import { TaxCalculator } from './components/TaxCalculator';

type ActiveTab = 'dashboard' | 'documents' | 'calculator';

function App() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('dashboard');
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const tabs = [
    { id: 'dashboard' as const, label: 'Dashboard', icon: Home },
    { id: 'documents' as const, label: 'Documents', icon: FileText },
    { id: 'calculator' as const, label: 'Tax Calculator', icon: Calculator },
  ];

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'documents':
        return (
          <div className="space-y-6">
            <FileUpload onUploadComplete={() => window.location.reload()} />
            <DocumentList />
          </div>
        );
      case 'calculator':
        return <TaxCalculator />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out lg:translate-x-0 lg:static lg:inset-0
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex items-center justify-between h-16 px-6 border-b">
          <h1 className="text-xl font-bold text-blue-600">Numeri</h1>
          <button
            onClick={() => setSidebarOpen(false)}
            className="lg:hidden"
          >
            <X size={24} />
          </button>
        </div>
        
        <nav className="mt-6">
          <div className="px-3">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => {
                    setActiveTab(tab.id);
                    setSidebarOpen(false);
                  }}
                  className={`
                    w-full flex items-center px-3 py-3 text-left rounded-lg transition-colors mb-1
                    ${activeTab === tab.id 
                      ? 'bg-blue-50 text-blue-600 font-medium' 
                      : 'text-gray-700 hover:bg-gray-50'
                    }
                  `}
                >
                  <Icon size={20} className="mr-3" />
                  {tab.label}
                </button>
              );
            })}
          </div>
        </nav>

        <div className="absolute bottom-0 left-0 right-0 p-6 border-t bg-gray-50">
          <div className="text-sm text-gray-600">
            <div className="font-medium">ATO Tax Preparation</div>
            <div>2024-25 Financial Year</div>
          </div>
        </div>
      </div>

      {/* Main content */}
      <div className="lg:pl-64">
        {/* Header */}
        <header className="bg-white shadow-sm border-b">
          <div className="flex items-center justify-between h-16 px-6">
            <div className="flex items-center">
              <button
                onClick={() => setSidebarOpen(true)}
                className="lg:hidden mr-3"
              >
                <Menu size={24} />
              </button>
              <h2 className="text-lg font-semibold text-gray-900">
                {tabs.find(tab => tab.id === activeTab)?.label}
              </h2>
            </div>
            <div className="text-sm text-gray-600">
              Welcome to Numeri Tax Preparation
            </div>
          </div>
        </header>

        {/* Main content area */}
        <main className="p-6">
          {renderActiveTab()}
        </main>
      </div>
    </div>
  );
}

export default App;
