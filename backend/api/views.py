from django.shortcuts import render
import pandas as pd
import json
from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

EXCEL_PATH = "api/Sample_data.xlsx"

@csrf_exempt
def download_data(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            query = body.get("query", "").strip().lower()
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        df = pd.read_excel(EXCEL_PATH)

        # Filter by location or city
        filtered_df = df[
            df['final location'].str.lower().str.contains(query, na=False) |
            df['city'].str.lower().str.contains(query, na=False)
        ]

        if filtered_df.empty:
            return JsonResponse({"error": "No data to download"}, status=404)

        # Prepare CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{query}_data.csv"'
        filtered_df.to_csv(response, index=False)
        return response

    return JsonResponse({"error": "Invalid method"}, status=405)

@csrf_exempt
def analyze_query(request):
    if request.method == "POST":
        # Load the Excel file
        df = pd.read_excel(EXCEL_PATH)

        # Parse JSON body
        try:
            body = json.loads(request.body)
        except json.JSONDecodeError:
            body = {}

        query = body.get("query", "").strip().lower()
        if not query:
            return JsonResponse({"error": "No query provided"}, status=400)

        # Remove "analyze " prefix if user typed "Analyze Akurdi"
        if query.startswith("analyze "):
            query = query.replace("analyze ", "")

        # Filter by final location or city (case-insensitive)
        filtered_df = df[
            df['final location'].str.lower().str.contains(query, na=False) |
            df['city'].str.lower().str.contains(query, na=False)
        ]

        # Summary
        total_sales = filtered_df['total_sales - igr'].sum() if not filtered_df.empty else 0
        summary = f"{len(filtered_df)} records found for '{query.title()}'. Total sales: {total_sales:,.0f}"

        # Chart: total sales per year
        if not filtered_df.empty:
            chart_df = filtered_df.groupby('year')['total_sales - igr'].sum().reset_index()
            chart_data = chart_df.to_dict(orient='records')
        else:
            chart_data = []

        # Table: select key columns
        table_columns = [
            'final location', 'year', 'city', 'total_sales - igr',
            'total sold - igr', 'flat_sold - igr', 'office_sold - igr',
            'shop_sold - igr', 'residential_sold - igr',
            'flat - weighted average rate', 'office - weighted average rate',
            'shop - weighted average rate'
        ]
        table_data = filtered_df[table_columns].to_dict(orient='records') if not filtered_df.empty else []

        return JsonResponse({
            "summary": summary,
            "chart": chart_data,
            "table": table_data
        })
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)
