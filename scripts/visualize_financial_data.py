import json
import matplotlib.pyplot as plt
import pandas as pd

def load_and_visualize_data():
    # Sample data for demonstration (we'll replace this with real API data later)
    sample_data = {
        "MSFT": {"market_cap": 3366494667000, "revenue": 270010008000},
        "GOOG": {"market_cap": 2014781243000, "revenue": 359713014000},
        "JPM": {"market_cap": 738237481000, "revenue": 168713994000},
        "BAC": {"market_cap": 336976314000, "revenue": 97452999000},
        "C": {"market_cap": 141144670000, "revenue": 71819002000},
        "PLD": {"market_cap": 99844841000, "revenue": 8733704000},
        "AMT": {"market_cap": 95734219000, "revenue": 10177400000},
        "SPG": {"market_cap": 60787261000, "revenue": 5994220000},
        "EQH": {"market_cap": 16319162000, "revenue": 15105000000}
    }
    
    # Create DataFrame
    df = pd.DataFrame.from_dict(sample_data, orient='index')
    
    # Sort by market cap
    df = df.sort_values('market_cap', ascending=True)
    
    # Convert market cap to billions for better readability
    df['market_cap_billions'] = df['market_cap'] / 1e9
    df['revenue_billions'] = df['revenue'] / 1e9
    
    # Create market cap visualization
    plt.figure(figsize=(12, 6))
    bars = plt.barh(df.index, df['market_cap_billions'])
    plt.xlabel('Market Cap (Billion USD)')
    plt.title('Company Market Capitalization Comparison')
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2,
                f'${width:,.0f}B',
                ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('data/market_cap_visualization.png')
    print("\nVisualization saved as 'data/market_cap_visualization.png'")
    
    # Print summary statistics
    print("\nMarket Cap Summary Statistics (in billions USD):")
    stats = df['market_cap_billions'].describe()
    print(stats.round(2))
    
    print("\nRevenue Summary Statistics (in billions USD):")
    stats = df['revenue_billions'].describe()
    print(stats.round(2))
    
    # Create a second visualization for revenue comparison
    plt.figure(figsize=(12, 6))
    bars = plt.barh(df.index, df['revenue_billions'])
    plt.xlabel('Revenue (Billion USD)')
    plt.title('Company Revenue Comparison')
    
    # Add value labels
    for bar in bars:
        width = bar.get_width()
        plt.text(width, bar.get_y() + bar.get_height()/2,
                f'${width:,.0f}B',
                ha='left', va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('data/revenue_visualization.png')
    print("\nRevenue visualization saved as 'data/revenue_visualization.png'")

if __name__ == "__main__":
    load_and_visualize_data()
