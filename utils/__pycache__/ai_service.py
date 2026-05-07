import google.generativeai as genai
import os
from dotenv import load_dotenv
import pandas as pd
import json
import streamlit as st

load_dotenv()

class AIInsightEngine:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=api_key)
        
        # Use Gemini 1.5 Flash (fastest and free)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("🤖 Using Google Gemini 1.5 Flash (FREE)")
    
    def _make_completion(self, prompt):
        """Make API call to Gemini"""
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ Error: {str(e)}\n\nPlease check your GEMINI_API_KEY in .env file."
    
    def analyze_country(self, df, country_name):
        """Generate AI insights for a specific country"""
        country_data = df[df['country_name'] == country_name].sort_values('year')
        
        if len(country_data) == 0:
            return "No data available for this country."
        
        stats = {
            'country': country_name,
            'avg_gini': float(country_data['gini_index'].mean()),
            'min_gini': float(country_data['gini_index'].min()),
            'max_gini': float(country_data['gini_index'].max()),
            'latest_gini': float(country_data['gini_index'].iloc[-1]),
            'earliest_year': int(country_data['year'].min()),
            'latest_year': int(country_data['year'].max()),
            'trend': 'increasing' if country_data['gini_index'].iloc[-1] > country_data['gini_index'].iloc[0] else 'decreasing'
        }
        
        prompt = f"""
        As an expert economist, analyze the income inequality data for {country_name}:
        
        📊 Data Summary:
        - Average Gini Index: {stats['avg_gini']:.2f}
        - Range: {stats['min_gini']:.2f} to {stats['max_gini']:.2f}
        - Latest Gini Index ({stats['latest_year']}): {stats['latest_gini']:.2f}
        - Overall trend: {stats['trend']}
        - Time period: {stats['earliest_year']} to {stats['latest_year']}
        
        Please provide a comprehensive analysis including:
        
        1. **Assessment**: Brief evaluation of the country's inequality level (2-3 sentences)
        
        2. **Trend Analysis**: What does the {stats['trend']} trend indicate? (2-3 sentences)
        
        3. **Economic & Social Implications**: 
           - What are 3 key implications of this inequality level?
        
        4. **Policy Recommendations**: 
           - Provide 3 specific, actionable policy recommendations
        
        Format your response with clear headings and bullet points.
        Be professional, data-driven, and actionable.
        """
        
        return self._make_completion(prompt)
    
    def compare_countries(self, df, countries):
        """AI-powered comparison of multiple countries"""
        comparison_data = []
        
        for country in countries:
            country_df = df[df['country_name'] == country]
            if len(country_df) > 0:
                comparison_data.append({
                    'country': country,
                    'avg_gini': float(country_df['gini_index'].mean()),
                    'latest_gini': float(country_df['gini_index'].iloc[-1]),
                    'trend': 'increasing' if country_df['gini_index'].iloc[-1] > country_df['gini_index'].iloc[0] else 'decreasing'
                })
        
        prompt = f"""
        Compare the income inequality patterns across these countries:
        
        {json.dumps(comparison_data, indent=2)}
        
        Provide a detailed comparison including:
        
        1. **Overview**: Key similarities and differences (3-4 points)
        
        2. **Rankings**: 
           - Which country has the most inequality?
           - Which has the least?
           - Explain why
        
        3. **Notable Trends**: What patterns do you observe?
        
        4. **Root Causes**: What might explain these differences? (3-4 factors)
        
        5. **Lessons Learned**: What can countries learn from each other?
        
        Be specific, data-driven, and use clear formatting with headings and bullet points.
        """
        
        return self._make_completion(prompt)
    
    def predict_trends(self, df, country_name, years_ahead=5):
        """AI-powered trend prediction and analysis"""
        country_data = df[df['country_name'] == country_name].sort_values('year')
        
        if len(country_data) < 5:
            return "⚠️ Insufficient data for trend prediction. At least 5 data points required."
        
        recent_data = country_data.tail(10)[['year', 'gini_index']].to_dict('records')
        
        prompt = f"""
        Based on this historical Gini Index data for {country_name}:
        
        {json.dumps(recent_data, indent=2)}
        
        Provide a comprehensive trend forecast:
        
        1. **Pattern Analysis**: Analyze the recent trend pattern in detail
        
        2. **{years_ahead}-Year Forecast**: 
           - What's the likely direction?
           - Provide a range estimate
           - Explain your reasoning
        
        3. **Risk Factors**: 
           - Identify 4-5 key factors that could change this trajectory
           - Categorize as economic, social, or political
        
        4. **Early Warning Indicators**: 
           - What should policymakers monitor?
           - Suggest 3-4 specific metrics
        
        5. **Proactive Interventions**: 
           - Recommend 3-4 preventive policy measures
        
        Be realistic and acknowledge uncertainty. Use clear headings and formatting.
        """
        
        return self._make_completion(prompt)
    
    def answer_question(self, df, question):
        """Answer user questions about the data using AI"""
        data_summary = {
            'total_countries': len(df['country_name'].unique()),
            'year_range': f"{int(df['year'].min())} to {int(df['year'].max())}",
            'avg_global_gini': float(df['gini_index'].mean()),
            'total_records': len(df)
        }
        
        prompt = f"""
        You are an expert economist with access to a global income inequality database.
        
        📊 Database Summary:
        {json.dumps(data_summary, indent=2)}
        
        🙋 User Question: {question}
        
        Please provide a clear, accurate, and comprehensive answer:
        - Use the data context provided
        - Be specific and educational
        - Include examples where relevant
        - If the question requires analysis beyond the summary, explain what additional data would be needed
        - Use bullet points and clear formatting
        
        Aim for 4-6 sentences or equivalent bullet points.
        """
        
        return self._make_completion(prompt)
