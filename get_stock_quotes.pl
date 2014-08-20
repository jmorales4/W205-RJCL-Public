#
# get_stock_quotes.pl: Perl Script that reads Stock Quotes from Yahoo Finance API and writes them to AWS S3 every
# 10 minutes
#
use Finance::YahooQuote;
use Amazon::S3;
use strict;

### Global params
$Finance::YahooQuote::TIMEOUT = 60;
my $aws_access_key_id = '';
my $aws_secret_access_key = '';

### Open S3 connection
my $s3 = Amazon::S3->new(
{   
	aws_access_key_id     => $aws_access_key_id,
	aws_secret_access_key => $aws_secret_access_key,
	retry                 => 1,
}
);
my $bucket = $s3->bucket('rjcl-stockquotes');

### read in stock ticker symbols of interest
open INPUT, "stock_tickers.txt";
my @tickers;
foreach (<INPUT>)
{
	chomp($_);
	push(@tickers,$_);
}

close INPUT;

while(1)
{
	my $date_string = get_date_string();
	my $filename = "stock_quotes_".$date_string.".txt";
	my $filepath = "//home//ubuntu//rjcl_stockquotes//$filename";
	open OUTPUT, "> $filepath";
	print OUTPUT "0 Symbol|1 Company Name|2 Last Price|3 Last Trade Date|4 Last Trade Time|5 Change",
	    "|6 Percent Change|7 Volume|8 Average Daily Vol|9 Bid|10 Ask|11 Previous Close|12 Today's Open",
	    "|13 Day's Range|14 52-Week Range|15 Earnings per Share|16 P/E Ratio|17 Dividend Pay Date",
	    "|18 Dividend per Share|19 Dividend Yield|20 Market Capitalization|21 Stock Exchange\n";
	foreach my $symbol (@tickers)
	{
		my @quote = getonequote $symbol; # Get a quote for a single symbol
		print OUTPUT join("|",@quote),"\n";
	}
	close OUTPUT;
	
	$bucket->add_key_filename(
		$filename,$filename,
		{   content_type        => 'text/plain'}
		);
	sleep 600;
}

exit();

sub get_date_string
{
	my @date = localtime;
	my $day = $date[3];
	my $month = $date[4]+1;
	my $year = $date[5]+1900;
	my $hour = $date[2];
	my $min = $date[1];
	my $sec = $date[0];
	$day = "0".$day if(length($day) == 1);
	$month = "0".$month if(length($month) == 1);
	$hour = "0".$hour if(length($hour) == 1);
	$min = "0".$min if(length($min) == 1);
	$sec = "0".$sec if(length($sec) == 1);
	my $date_string = $year.$month.$day.$hour.$min.$sec;
	
	return $date_string;
}