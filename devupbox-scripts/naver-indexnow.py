import json
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

urls = [
    "https://devupbox.com/finance/car-insurance-comparison-2026",
    "https://devupbox.com/finance/real-loss-insurance-2026",
    "https://devupbox.com/finance/driver-insurance-guide-2026",
    "https://devupbox.com/finance/credit-score-improve-2026",
    "https://devupbox.com/finance/savings-interest-rate-2026",
    "https://devupbox.com/finance/isa-account-guide-2026",
    "https://devupbox.com/loan/youth-jeonse-loan-2026",
    "https://devupbox.com/loan/mortgage-rate-comparison-2026",
    "https://devupbox.com/loan/personal-loan-low-rate-2026",
    "https://devupbox.com/loan/jeonse-loan-refinance-guide",
    "https://devupbox.com/loan/small-business-gov-loan-2026",
    "https://devupbox.com/finance/cancer-insurance-2026",
    "https://devupbox.com/finance/dental-insurance-2026",
    "https://devupbox.com/finance/prenatal-insurance-2026",
    "https://devupbox.com/finance/travel-insurance-2026",
    "https://devupbox.com/finance/fire-insurance-guide-2026",
    "https://devupbox.com/foreign-car/long-term-rent-vs-lease-2026",
    "https://devupbox.com/foreign-car/imported-car-maintenance-cost-ranking",
    "https://devupbox.com/foreign-car/car-lease-pros-cons-guide",
    "https://devupbox.com/foreign-car/benz-e-class-maintenance-cost",
    "https://devupbox.com/foreign-car/bmw-3-vs-benz-c-2026",
    "https://devupbox.com/finance/income-tax-filing-guide-2026",
    "https://devupbox.com/finance/year-end-tax-refund-tips-2026",
    "https://devupbox.com/finance/vat-filing-guide-2026",
    "https://devupbox.com/finance/gift-tax-exemption-2026",
    "https://devupbox.com/finance/inheritance-tax-guide-2026",
    "https://devupbox.com/kin/implant-cost-comparison-2026",
    "https://devupbox.com/kin/lasik-lasek-comparison-2026",
    "https://devupbox.com/kin/health-checkup-guide-2026",
    "https://devupbox.com/kin/manual-therapy-cost-guide-2026",
    "https://devupbox.com/kin/dental-scaling-cost-insurance-2026",
    "https://devupbox.com/finance/etf-recommendation-2026",
    "https://devupbox.com/finance/dividend-stock-2026",
    "https://devupbox.com/finance/stock-beginner-guide-2026",
    "https://devupbox.com/finance/cma-account-comparison-2026",
    "https://devupbox.com/finance/gold-investment-guide-2026",
    "https://devupbox.com/finance/housing-subscription-guide-2026",
    "https://devupbox.com/finance/jeonse-vs-monthly-rent-2026",
    "https://devupbox.com/finance/real-estate-commission-2026",
    "https://devupbox.com/finance/jeonse-fraud-prevention-guide",
    "https://devupbox.com/finance/redevelopment-reconstruction-guide",
    "https://devupbox.com/info/vpn-recommendation-2026",
    "https://devupbox.com/info/laptop-recommendation-2026",
    "https://devupbox.com/info/cloud-storage-comparison-2026",
    "https://devupbox.com/info/budget-phone-plan-2026",
    "https://devupbox.com/info/internet-provider-comparison-2026",
    "https://devupbox.com/kin/severance-pay-calculation-guide",
    "https://devupbox.com/kin/unemployment-benefit-guide-2026",
    "https://devupbox.com/kin/certification-recommendation-2026",
    "https://devupbox.com/kin/moving-cost-guide-2026",
    "https://devupbox.com/kin/certified-letter-guide",
]

payload = {
    "host": "devupbox.com",
    "key": "8dbbd7d6729b4a65b7dce4b9083c65e3",
    "keyLocation": "https://devupbox.com/8dbbd7d6729b4a65b7dce4b9083c65e3.txt",
    "urlList": urls
}

data = json.dumps(payload).encode("utf-8")

# Naver IndexNow
req = urllib.request.Request(
    "https://searchadvisor.naver.com/indexnow",
    data=data,
    method="POST"
)
req.add_header("Content-Type", "application/json; charset=utf-8")

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        print(f"Naver IndexNow: HTTP {resp.status}")
        print(f"Response: {resp.read().decode()}")
except urllib.error.HTTPError as e:
    print(f"Naver IndexNow: HTTP {e.code}")
    print(f"Response: {e.read().decode()}")

# Bing/Yandex IndexNow (bonus - same protocol)
for engine_name, engine_url in [("Bing", "https://www.bing.com/indexnow"), ("Yandex", "https://yandex.com/indexnow")]:
    req2 = urllib.request.Request(engine_url, data=data, method="POST")
    req2.add_header("Content-Type", "application/json; charset=utf-8")
    try:
        with urllib.request.urlopen(req2, timeout=30) as resp:
            print(f"{engine_name} IndexNow: HTTP {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"{engine_name} IndexNow: HTTP {e.code}")
    except Exception as e:
        print(f"{engine_name} IndexNow: {e}")

print(f"\nTotal URLs submitted: {len(urls)}")
