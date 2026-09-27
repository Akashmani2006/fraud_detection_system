from app.tools.merchant_tools import get_merchant_risk


print("M101:")
print(get_merchant_risk("M101"))

print()

print("M501:")
print(get_merchant_risk("M501"))

print()

print("Unknown merchant:")
print(get_merchant_risk("M999"))