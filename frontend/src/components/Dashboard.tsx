import React, { useEffect, useState } from 'react';
import { DollarSign, FileText, Calculator, TrendingUp } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from './ui';
import { documentsApi, taxCalculatorApi } from '../lib/api';
import { formatCurrency } from '../lib/utils';
import type { Document, TaxInfo } from '../types';

export const Dashboard: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [taxInfo, setTaxInfo] = useState<TaxInfo | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const [docs, brackets] = await Promise.all([
        documentsApi.list(),
        taxCalculatorApi.getBrackets(),
      ]);
      setDocuments(docs);
      setTaxInfo(brackets);
    } catch (error) {
      console.error('Failed to load dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const completedDocuments = documents.filter(doc => doc.status === 'completed');
  const processingDocuments = documents.filter(doc => doc.status === 'processing');

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <Card key={i}>
            <CardContent className="p-6">
              <div className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div className="h-8 bg-gray-200 rounded w-1/2"></div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Documents</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{documents.length}</div>
            <p className="text-xs text-muted-foreground">
              {completedDocuments.length} processed
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Processing</CardTitle>
            <Calculator className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{processingDocuments.length}</div>
            <p className="text-xs text-muted-foreground">
              Documents being processed
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tax Year</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{taxInfo?.tax_year || '2024-25'}</div>
            <p className="text-xs text-muted-foreground">
              Current tax year
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Tax-Free Threshold</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{formatCurrency(18200)}</div>
            <p className="text-xs text-muted-foreground">
              For {taxInfo?.tax_year || '2024-25'}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Tax Brackets Overview */}
      {taxInfo && (
        <Card>
          <CardHeader>
            <CardTitle>2024-25 Tax Brackets</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {taxInfo.brackets.map((bracket, index) => (
                <div key={index} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                  <div>
                    <div className="font-medium">
                      {formatCurrency(bracket.min)} - {bracket.max ? formatCurrency(bracket.max) : 'and above'}
                    </div>
                    <div className="text-sm text-gray-600">{bracket.description}</div>
                  </div>
                  <div className="text-lg font-bold">
                    {(bracket.rate * 100).toFixed(1)}%
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 pt-4 border-t">
              <div className="text-center">
                <div className="text-sm text-gray-600">Medicare Levy</div>
                <div className="font-semibold">{(taxInfo.medicare_levy.rate * 100)}%</div>
              </div>
              <div className="text-center">
                <div className="text-sm text-gray-600">Work from Home Rate</div>
                <div className="font-semibold">{formatCurrency(taxInfo.work_from_home_rate)}/hour</div>
              </div>
              <div className="text-center">
                <div className="text-sm text-gray-600">Instant Asset Write-off</div>
                <div className="font-semibold">{formatCurrency(taxInfo.instant_asset_writeoff)}</div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};