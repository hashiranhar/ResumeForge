<script>
    
import React, { useState, useEffect } from 'react';
import { BarChart3, Zap, FileText, AlertTriangle, CheckCircle, Clock } from 'lucide-react';

const UsageDashboardWidget = ({ className = "" }) => {
  const [usageData, setUsageData] = useState(null);
  const [loading, setLoading] = useState(true);

  // Mock data - replace with actual API call
  useEffect(() => {
    const fetchUsage = async () => {
      // Simulate API call
      setTimeout(() => {
        setUsageData({
          api_calls: {
            used: 23,
            limit: 50,
            remaining: 27,
            percentage: 46,
            warning_level: "medium"
          },
          cvs: {
            used: 8,
            limit: 10,
            remaining: 2,
            percentage: 80,
            warning_level: "high"
          },
          reset_info: "API calls reset daily at midnight UK time"
        });
        setLoading(false);
      }, 1000);
    };
    
    fetchUsage();
  }, []);

  const getProgressColor = (warningLevel) => {
    switch (warningLevel) {
      case 'low': return 'bg-green-500';
      case 'medium': return 'bg-yellow-500';
      case 'high': return 'bg-red-500';
      default: return 'bg-gray-300';
    }
  };

  const getStatusIcon = (warningLevel) => {
    switch (warningLevel) {
      case 'low': return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'medium': return <AlertTriangle className="h-4 w-4 text-yellow-500" />;
      case 'high': return <AlertTriangle className="h-4 w-4 text-red-500" />;
      default: return <CheckCircle className="h-4 w-4 text-gray-400" />;
    }
  };

  if (loading) {
    return (
      <div className={`bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 ${className}`}>
        <div className="animate-pulse">
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-5 h-5 bg-gray-300 rounded"></div>
            <div className="w-24 h-4 bg-gray-300 rounded"></div>
          </div>
          <div className="space-y-3">
            <div className="w-full h-3 bg-gray-300 rounded"></div>
            <div className="w-full h-3 bg-gray-300 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 p-4 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <BarChart3 className="h-5 w-5 text-gray-500 dark:text-gray-400" />
          <h3 className="font-medium text-gray-900 dark:text-white">Usage Overview</h3>
        </div>
      </div>

      {/* Usage Metrics */}
      <div className="space-y-4">
        {/* API Calls */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <Zap className="h-4 w-4 text-blue-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                API Calls
              </span>
              {getStatusIcon(usageData.api_calls.warning_level)}
            </div>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {usageData.api_calls.used}/{usageData.api_calls.limit}
            </span>
          </div>
          
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div 
              className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(usageData.api_calls.warning_level)}`}
              style={{ width: `${usageData.api_calls.percentage}%` }}
            ></div>
          </div>
          
          <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>{usageData.api_calls.remaining} remaining</span>
            <span>{usageData.api_calls.percentage}% used</span>
          </div>
        </div>

        {/* CVs */}
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <FileText className="h-4 w-4 text-green-500" />
              <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                CVs Created
              </span>
              {getStatusIcon(usageData.cvs.warning_level)}
            </div>
            <span className="text-sm text-gray-600 dark:text-gray-400">
              {usageData.cvs.used}/{usageData.cvs.limit}
            </span>
          </div>
          
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div 
              className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(usageData.cvs.warning_level)}`}
              style={{ width: `${usageData.cvs.percentage}%` }}
            ></div>
          </div>
          
          <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>{usageData.cvs.remaining} remaining</span>
            <span>{usageData.cvs.percentage}% used</span>
          </div>
        </div>
      </div>

      {/* Reset Info */}
      <div className="mt-4 pt-3 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
          <Clock className="h-3 w-3" />
          <span>{usageData.reset_info}</span>
        </div>
      </div>

      {/* Action Buttons */}
      {(usageData.api_calls.warning_level === 'high' || usageData.cvs.warning_level === 'high') && (
        <div className="mt-3">
          <button className="w-full text-sm bg-blue-600 text-white px-3 py-2 rounded-md hover:bg-blue-700 transition-colors">
            Upgrade Plan
          </button>
        </div>
      )}
    </div>
  );
};

export default UsageDashboardWidget;
</script>