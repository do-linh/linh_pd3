class OrderStatus:
    DRAFT = "draft"  # fully editable, not confirmed order created by staff users
    UNFULFILLED = "unfulfilled"  # order with no items marked as fulfilled
    PARTIALLY_FULFILLED = (
        "partially fulfilled"  # order with some items marked as fulfilled
    )
    FULFILLED = "fulfilled"  # order with all items marked as fulfilled
    CANCELED = "canceled"  # permanently canceled order

    CHOICES = [
        (DRAFT, "Draft"),
        (UNFULFILLED, "Unfulfilled"),
        (PARTIALLY_FULFILLED, "Partially fulfilled"),
        (FULFILLED, "Fulfilled"),
        (CANCELED, "Canceled"),
    ]
class DiscountValueType:
    FIXED = "fixed"
    PERCENTAGE = "percentage"

    CHOICES = [
        (FIXED, "đ"),
        (PERCENTAGE, "%"),
    ]
class VoucherType:
    SHIPPING = "shipping"
    ENTIRE_ORDER = "entire_order"
    SPECIFIC_PRODUCT = "specific_product"

    CHOICES = [
        (ENTIRE_ORDER, "Entire order"),
        (SHIPPING, "Shipping"),
        (SPECIFIC_PRODUCT, "Specific products, collections and categories"),
    ]