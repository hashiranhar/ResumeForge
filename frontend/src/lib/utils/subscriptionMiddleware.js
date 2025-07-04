// subscriptionMiddleware.js
import { get } from "svelte/store";
import {
  currentSubscription,
  usageData,
  subscriptionService,
} from "$lib/stores/subscription.js";
import { authenticatedFetch } from "$lib/stores/auth.js";
import { addToast } from "$lib/stores/toast.js";

// Enhanced fetch wrapper that handles subscription limits
export async function subscriptionAwareFetch(url, options = {}) {
  const response = await authenticatedFetch(url, options);

  // Handle 429 Too Many Requests
  if (response.status === 429) {
    const errorData = await response.json();

    return {
      ok: false,
      status: 429,
      limitError: errorData.detail,
      json: () => Promise.resolve(errorData),
    };
  }

  return response;
}

// Usage checking utilities
export const usageChecker = {
  // Check if user can make API calls
  canMakeAPICall() {
    const usage = get(usageData);
    const subscription = get(currentSubscription);

    if (!usage || !subscription) return false;

    return usage.api_calls.used < usage.api_calls.limit;
  },

  // Check if user can create CVs
  canCreateCV() {
    const usage = get(usageData);
    const subscription = get(currentSubscription);

    if (!usage || !subscription) return false;

    return usage.cvs.used < usage.cvs.limit;
  },

  // Get current API usage percentage
  getAPIUsagePercentage() {
    const usage = get(usageData);
    if (!usage) return 0;

    return (usage.api_calls.used / usage.api_calls.limit) * 100;
  },

  // Get current CV usage percentage
  getCVUsagePercentage() {
    const usage = get(usageData);
    if (!usage) return 0;

    return (usage.cvs.used / usage.cvs.limit) * 100;
  },

  // Get warning level for usage
  getUsageWarningLevel(percentage) {
    if (percentage >= 90) return "high";
    if (percentage >= 70) return "medium";
    return "low";
  },
};

// Pre-flight checks for different actions
export const actionChecks = {
  // Check before making LLM requests
  async checkBeforeLLMRequest() {
    if (!usageChecker.canMakeAPICall()) {
      const usage = get(usageData);
      return {
        allowed: false,
        reason: "api_limit",
        data: {
          current: usage?.api_calls.used || 0,
          limit: usage?.api_calls.limit || 0,
        },
      };
    }

    return { allowed: true };
  },

  // Check before creating CV
  async checkBeforeCVCreation() {
    if (!usageChecker.canCreateCV()) {
      const usage = get(usageData);
      return {
        allowed: false,
        reason: "cv_limit",
        data: {
          current: usage?.cvs.used || 0,
          limit: usage?.cvs.limit || 0,
        },
      };
    }

    return { allowed: true };
  },
};

// Usage tracking
export const usageTracker = {
  // Increment API usage locally (optimistic update)
  incrementAPIUsage() {
    usageData.update((usage) => {
      if (usage) {
        return {
          ...usage,
          api_calls: {
            ...usage.api_calls,
            used: usage.api_calls.used + 1,
            remaining: Math.max(0, usage.api_calls.remaining - 1),
            percentage: Math.min(
              100,
              ((usage.api_calls.used + 1) / usage.api_calls.limit) * 100
            ),
          },
        };
      }
      return usage;
    });
  },

  // Increment CV usage locally
  incrementCVUsage() {
    usageData.update((usage) => {
      if (usage) {
        return {
          ...usage,
          cvs: {
            ...usage.cvs,
            used: usage.cvs.used + 1,
            remaining: Math.max(0, usage.cvs.remaining - 1),
            percentage: Math.min(
              100,
              ((usage.cvs.used + 1) / usage.cvs.limit) * 100
            ),
          },
        };
      }
      return usage;
    });
  },

  // Refresh usage from server
  async refreshUsage() {
    await subscriptionService.loadUsage();
  },
};

// Subscription status helpers
export const subscriptionHelpers = {
  // Check if user has access to feature
  hasFeatureAccess(feature) {
    const subscription = get(currentSubscription);
    if (!subscription) return false;

    const featureMap = {
      ai_chat: ["basic", "pro"],
      ats_analysis: ["basic", "pro"],
      inline_editing: ["basic", "pro"],
      premium_templates: ["basic", "pro"],
      priority_support: ["basic", "pro"],
      advanced_export: ["pro"],
      unlimited_ai: ["pro"],
    };

    return featureMap[feature]?.includes(subscription.name) || false;
  },

  // Get plan limits
  getPlanLimits(planName = null) {
    const subscription = get(currentSubscription);
    const plan = planName || subscription?.name || "free";

    const limits = {
      free: { api_calls: 5, cvs: 3 },
      basic: { api_calls: 25, cvs: 10 },
      pro: { api_calls: 50, cvs: 50 },
    };

    return limits[plan] || limits.free;
  },

  // Check if user is on specific plan
  isOnPlan(planName) {
    const subscription = get(currentSubscription);
    return subscription?.name === planName;
  },

  // Check if user can upgrade
  canUpgrade() {
    const subscription = get(currentSubscription);
    return !subscription || subscription.name !== "pro";
  },
};
