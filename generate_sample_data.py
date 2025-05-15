from data_generator import TradeDataGenerator
import pandas as pd
import json
import os

def generate_and_save_data():
    # Create output directory if it doesn't exist
    output_dir = 'sample_data'
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize data generator
    generator = TradeDataGenerator()
    
    # Generate trade data
    print("Generating trade data...")
    trade_data = generator.generate_trade_data(years=5)
    trade_data.to_csv(os.path.join(output_dir, 'trade_data.csv'), index=False)
    print(f"Generated {len(trade_data)} trade records")
    
    # Generate market insights
    print("\nGenerating market insights...")
    market_insights = {
        country: generator.generate_market_insights(country)
        for country in generator.countries[:10]
    }
    with open(os.path.join(output_dir, 'market_insights.json'), 'w') as f:
        json.dump(market_insights, f, indent=2)
    print(f"Generated insights for {len(market_insights)} countries")
    
    # Generate sample reports
    print("\nGenerating sample reports...")
    sample_reports = {
        country: generator.generate_report_data(country, 2023)
        for country in generator.countries[:5]
    }
    with open(os.path.join(output_dir, 'sample_reports.json'), 'w') as f:
        json.dump(sample_reports, f, indent=2)
    print(f"Generated {len(sample_reports)} sample reports")
    
    print("\nSample data generation complete!")
    print(f"Files saved in '{output_dir}' directory:")

if __name__ == "__main__":
    generate_and_save_data() 