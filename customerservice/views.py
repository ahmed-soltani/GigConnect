from django.shortcuts import render, redirect, get_object_or_404
from customerservice.decorators import cs_required
from reviews.models import ReviewReport


@cs_required
def cs_dashboard(request):
    # Only show unresolved reports
    reported_count = ReviewReport.objects.filter(is_resolved=False).count()
    return render(request, "customerservice/dashboard.html", {"reported_count": reported_count})


@cs_required
def cs_reports(request):
    # Resolve a report
    if request.method == "POST" and "resolve" in request.POST:
        report_id = request.POST.get("resolve")
        report = get_object_or_404(ReviewReport, id=report_id)
        report.is_resolved = True
        report.save()
        return redirect("cs_reports")

    reports = (
        ReviewReport.objects
        .filter(is_resolved=False)
        .select_related("review", "review__product", "reporter")
        .order_by("-timestamp")
    )
    return render(request, "customerservice/reported_reviews.html", {"reports": reports})
