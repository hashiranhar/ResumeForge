import { writable, derived } from "svelte/store";
import { authenticatedFetch } from "./auth.js";

// Subscription state
export const currentSubscription = writable(null);
export const availablePlans = writable([]);
export const usageData = writable(null);
export const isSubscriptionLoading = writable(false);
export const subscriptionError = writable(null);

// Derived stores
export const isFreeTier = derived(
  currentSubscription,
  ($subscription) => !$subscription || $subscription.name === "free"
);

export const isPremiumUser = derived(
  currentSubscription,
  ($subscription) =>
    $subscription && ["basic", "pro"].includes($subscription.name)
);

export const subscriptionService = {
  // Load current subscription
  async loadCurrentSubscription() {
    isSubscriptionLoading.set(true);
    subscriptionError.set(null);

    try {
      const response = await authenticatedFetch("/api/subscription/current");
      if (!response.ok) {
        throw new Error("Failed to load subscription");
      }

      const data = await response.json();
      currentSubscription.set(data);
      return { success: true, data };
    } catch (err) {
      subscriptionError.set(err.message);
      return { success: false, error: err.message };
    } finally {
      isSubscriptionLoading.set(false);
    }
  },

  // Load available plans
  async loadPlans() {
    try {
      const response = await fetch("/api/subscription/plans");
      if (!response.ok) {
        throw new Error("Failed to load plans");
      }

      const data = await response.json();
      availablePlans.set(data);
      return { success: true, data };
    } catch (err) {
      subscriptionError.set(err.message);
      return { success: false, error: err.message };
    }
  },

  // Load usage data
  async loadUsage() {
    try {
      const response = await authenticatedFetch("/api/subscription/usage");
      if (!response.ok) {
        throw new Error("Failed to load usage");
      }

      const data = await response.json();
      usageData.set(data);
      return { success: true, data };
    } catch (err) {
      subscriptionError.set(err.message);
      return { success: false, error: err.message };
    }
  },

  // Create checkout session
  async createCheckoutSession(planId, billingCycle = "monthly") {
    isSubscriptionLoading.set(true);

    try {
      const response = await authenticatedFetch("/api/subscription/checkout", {
        method: "POST",
        body: JSON.stringify({
          plan_id: planId,
          billing_cycle: billingCycle,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to create checkout session");
      }

      const data = await response.json();

      // Redirect to Stripe checkout
      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      }

      return { success: true, data };
    } catch (err) {
      subscriptionError.set(err.message);
      return { success: false, error: err.message };
    } finally {
      isSubscriptionLoading.set(false);
    }
  },

  // Cancel subscription
  async cancelSubscription() {
    isSubscriptionLoading.set(true);

    try {
      const response = await authenticatedFetch("/api/subscription/cancel", {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error("Failed to cancel subscription");
      }

      const data = await response.json();
      currentSubscription.set(data);
      return { success: true, data };
    } catch (err) {
      subscriptionError.set(err.message);
      return { success: false, error: err.message };
    } finally {
      isSubscriptionLoading.set(false);
    }
  },

  // Get dashboard data (subscription + usage)
  async loadDashboardData() {
    try {
      const response = await authenticatedFetch("/api/subscription/dashboard");
      if (!response.ok) {
        throw new Error("Failed to load dashboard data");
      }

      const data = await response.json();
      currentSubscription.set(data.subscription);
      usageData.set(data.usage);
      return { success: true, data };
    } catch (err) {
      subscriptionError.set(err.message);
      return { success: false, error: err.message };
    }
  },
};
