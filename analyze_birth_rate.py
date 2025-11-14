import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Set Korean font for matplotlib
try:
    plt.rc('font', family='Malgun Gothic')
    plt.rcParams['axes.unicode_minus'] = False # For displaying minus sign
except:
    print("Malgun Gothic font not found. Please install it for Korean characters to be displayed correctly.")

try:
    # 1. Load Data and Transpose
    file_path = r'C:\Users\student\Downloads\출생아수__합계출산율__자연증가_등_20251114151914.xlsx'
    df = pd.read_excel(file_path, header=None).T

    # 2. Data Cleansing
    # Set the first row as header
    df.columns = df.iloc[0]
    # Remove the header row from data
    df = df[1:]
    # Reset index
    df = df.reset_index(drop=True)

    # Rename columns for easier access
    df.rename(columns={'기본항목별': 'Year', '출생아수(명)': 'Newborns', '합계출산율(명)': 'FertilityRate'}, inplace=True)
    
    # Select only the necessary columns (ensure they exist)
    required_cols = ['Year', 'Newborns', 'FertilityRate']
    df = df[required_cols]

    # Convert data types
    for col in required_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with missing essential data
    df.dropna(subset=required_cols, inplace=True)
    
    # Convert Year to integer
    df['Year'] = df['Year'].astype(int)
    
    # Sort by year
    df.sort_values('Year', inplace=True)
    
    print("=" * 50)
    print("데이터 분석 및 시각화 결과")
    print("=" * 50)

    # 3. Data Analysis
    print("\n[기초 통계 요약]\n")
    # Format the describe output for better readability
    print(df[['Newborns', 'FertilityRate']].describe().apply(lambda s: s.apply('{:,.2f}'.format)))
    
    max_newborns_year = df.loc[df['Newborns'].idxmax()]
    min_newborns_year = df.loc[df['Newborns'].idxmin()]
    
    max_fertility_year = df.loc[df['FertilityRate'].idxmax()]
    min_fertility_year = df.loc[df['FertilityRate'].idxmin()]
    
    print(f"\n[주요 지표 분석]")
    print(f"- 최고 출생아 수: {max_newborns_year['Newborns']:,.0f}명 ({max_newborns_year['Year']}년)")
    print(f"- 최저 출생아 수: {min_newborns_year['Newborns']:,.0f}명 ({min_newborns_year['Year']}년)")
    print(f"- 최고 합계출산율: {max_fertility_year['FertilityRate']}명 ({max_fertility_year['Year']}년)")
    print(f"- 최저 합계출산율: {min_fertility_year['FertilityRate']}명 ({min_fertility_year['Year']}년)")
    
    correlation = df['Newborns'].corr(df['FertilityRate'])
    print(f"\n[상관관계 분석]")
    print(f"- 출생아 수와 합계출산율의 상관계수: {correlation:.2f}")
    print("  (1에 가까울수록 강한 양의 상관관계, -1에 가까울수록 강한 음의 상관관계)")
    print("\n")

    # 4. Visualization
    plt.figure(figsize=(14, 7))
    plt.plot(df['Year'], df['Newborns'], marker='o', linestyle='-')
    
    plt.title('연도별 출생아 수 변화 (1970-2023)', fontsize=16, pad=20)
    plt.xlabel('연도', fontsize=12)
    plt.ylabel('출생아 수 (명)', fontsize=12)
    
    # Add thousands separator to y-axis labels
    ax = plt.gca()
    ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, p: format(int(x), ',')))
    
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.xticks(rotation=45)
    # Set x-axis ticks to be more readable, e.g., every 5 years
    years = df['Year'].unique()
    plt.xticks(years[::5])
    plt.tight_layout()
    
    # Save the plot
    graph_path = 'birth_rate_graph.png'
    plt.savefig(graph_path)
    
    print("=" * 50)
    print(f"'{graph_path}' 파일로 그래프가 성공적으로 저장되었습니다.")
    print("=" * 50)

except FileNotFoundError:
    print(f"오류: 파일을 찾을 수 없습니다. 경로를 확인하세요: {file_path}")
except Exception as e:
    print(f"데이터 처리 중 오류가 발생했습니다: {e}")