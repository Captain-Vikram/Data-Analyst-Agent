"""
Visualization engine for the AI Data Analyst Agent.

This module contains the VisualizationEngine class that creates
professional-quality visualizations including correlation matrices,
summary dashboards, and various charts.
"""

from typing import Optional
import warnings
warnings.filterwarnings('ignore')

# Visualization libraries
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


class VisualizationEngine:
    """
    Creates visualizations for data analysis.
    
    This class provides methods to generate various types of visualizations
    including correlation matrices, summary dashboards, and statistical plots.
    """
    
    def __init__(self, agent):
        """
        Initialize the VisualizationEngine.
        
        Args:
            agent: DataAnalystAgent instance containing the data to visualize
        """
        self.agent = agent
    
    def create_summary_dashboard(self) -> Optional[plt.Figure]:
        """
        Create a comprehensive summary dashboard.
        
        Generates a 4-panel dashboard showing:
        - Data types distribution
        - Missing data patterns
        - Numeric columns distribution
        - Dataset information
        
        Returns:
            matplotlib Figure object or None if no data available
        """
        if self.agent.current_data is None:
            return None
        
        df = self.agent.current_data
        
        if df.empty:
            return None
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Data Summary Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Data types distribution
        dtype_counts = df.dtypes.value_counts()
        axes[0, 0].pie(dtype_counts.values, labels=dtype_counts.index, autopct='%1.1f%%')
        axes[0, 0].set_title('Data Types Distribution')
        
        # 2. Missing data pattern
        if df.isnull().sum().sum() > 0:
            sns.heatmap(df.isnull(), cbar=True, ax=axes[0, 1], cmap='viridis')
            axes[0, 1].set_title('Missing Data Pattern')
        else:
            axes[0, 1].text(0.5, 0.5, 'No Missing Data', ha='center', va='center', fontsize=14)
            axes[0, 1].set_title('Missing Data Pattern')
        
        # 3. Numeric columns distribution
        numeric_cols = df.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            # Show first few numeric columns
            cols_to_plot = numeric_cols[:4]  # Limit to 4 columns
            df[cols_to_plot].hist(bins=20, ax=axes[1, 0], alpha=0.7)
            axes[1, 0].set_title('Numeric Columns Distribution')
        else:
            axes[1, 0].text(0.5, 0.5, 'No Numeric Columns', ha='center', va='center', fontsize=14)
            axes[1, 0].set_title('Numeric Columns Distribution')
        
        # 4. Dataset info
        info_text = f"""Dataset Shape: {df.shape[0]} rows × {df.shape[1]} columns

Column Types:
{df.dtypes.value_counts().to_string()}

Memory Usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB

Missing Values: {df.isnull().sum().sum()}"""
        
        axes[1, 1].text(0.05, 0.95, info_text, transform=axes[1, 1].transAxes, 
                       fontsize=10, verticalalignment='top', fontfamily='monospace')
        axes[1, 1].set_xlim(0, 1)
        axes[1, 1].set_ylim(0, 1)
        axes[1, 1].set_title('Dataset Information')
        axes[1, 1].axis('off')
        
        plt.tight_layout()
        return fig
    
    def create_correlation_matrix(self) -> Optional[plt.Figure]:
        """
        Create correlation matrix for numeric columns.
        
        Generates a professional correlation heatmap showing relationships
        between all numeric variables in the dataset.
        
        Returns:
            matplotlib Figure object or None if no numeric data available
        """
        if self.agent.current_data is None:
            return None
        
        df = self.agent.current_data
        numeric_df = df.select_dtypes(include=['number'])
        
        if numeric_df.empty:
            return None
        
        fig, ax = plt.subplots(figsize=(12, 8))
        correlation_matrix = numeric_df.corr()
        
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                   square=True, linewidths=0.5, cbar_kws={"shrink": .5}, ax=ax)
        ax.set_title('Correlation Matrix of Numeric Variables', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        return fig
    
    def create_distribution_plot(self, column: str) -> Optional[plt.Figure]:
        """
        Create distribution plot for a specific column.
        
        Args:
            column: Name of the column to plot
            
        Returns:
            matplotlib Figure object or None if column not found
        """
        if self.agent.current_data is None or column not in self.agent.current_data.columns:
            return None
        
        df = self.agent.current_data
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if df[column].dtype in ['int64', 'float64']:
            # Numeric column - histogram
            ax.hist(df[column].dropna(), bins=30, alpha=0.7, edgecolor='black')
            ax.set_title(f'Distribution of {column}')
            ax.set_xlabel(column)
            ax.set_ylabel('Frequency')
        else:
            # Categorical column - bar plot
            value_counts = df[column].value_counts()
            ax.bar(range(len(value_counts)), value_counts.values)
            ax.set_title(f'Distribution of {column}')
            ax.set_xlabel(column)
            ax.set_ylabel('Count')
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
        
        plt.tight_layout()
        return fig
    
    def create_scatter_plot(self, x_col: str, y_col: str) -> Optional[plt.Figure]:
        """
        Create scatter plot between two columns.
        
        Args:
            x_col: Name of the x-axis column
            y_col: Name of the y-axis column
            
        Returns:
            matplotlib Figure object or None if columns not found
        """
        if (self.agent.current_data is None or 
            x_col not in self.agent.current_data.columns or
            y_col not in self.agent.current_data.columns):
            return None
        
        df = self.agent.current_data
        
        # Check if both columns are numeric
        if (df[x_col].dtype not in ['int64', 'float64'] or 
            df[y_col].dtype not in ['int64', 'float64']):
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.scatter(df[x_col], df[y_col], alpha=0.6)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f'Scatter Plot: {x_col} vs {y_col}')
        
        # Add correlation coefficient
        corr = df[x_col].corr(df[y_col])
        ax.text(0.05, 0.95, f'Correlation: {corr:.3f}', 
                transform=ax.transAxes, fontsize=12,
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        plt.tight_layout()
        return fig
    
    def create_box_plot(self, column: str, group_by: str = None) -> Optional[plt.Figure]:
        """
        Create box plot for a numeric column, optionally grouped by another column.
        
        Args:
            column: Name of the numeric column to plot
            group_by: Optional column name to group by
            
        Returns:
            matplotlib Figure object or None if column not found
        """
        if (self.agent.current_data is None or 
            column not in self.agent.current_data.columns):
            return None
        
        df = self.agent.current_data
        
        # Check if column is numeric
        if df[column].dtype not in ['int64', 'float64']:
            return None
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        if group_by and group_by in df.columns:
            # Grouped box plot
            groups = df.groupby(group_by)[column].apply(list)
            ax.boxplot(groups.values, labels=groups.index)
            ax.set_title(f'Box Plot of {column} by {group_by}')
            ax.set_xlabel(group_by)
            plt.xticks(rotation=45, ha='right')
        else:
            # Single box plot
            ax.boxplot(df[column].dropna())
            ax.set_title(f'Box Plot of {column}')
            ax.set_xticklabels([column])
        
        ax.set_ylabel(column)
        plt.tight_layout()
        return fig
