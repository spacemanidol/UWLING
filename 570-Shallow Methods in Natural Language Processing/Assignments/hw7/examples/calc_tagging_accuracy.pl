#!/usr/bin/env perl


## created on 12/13/05

## Purpose: calc "tagging" accuracy

## to run:
##    $0 gold_standard system_output


use strict;

my $delim = '\/';  ## word-tag delimiter


if(@ARGV != 2){
    die "usage: $0 gold_standard system_output\n";
}


open(my $gold_fp, "$ARGV[0]") or die "cannot open gold_standard_file $ARGV[0]\n";
open(my $sys_fp, "$ARGV[1]") or die "cannot open system_output $ARGV[1]\n";

my @gold_sents = ();
my @sys_sents = ();


my $sent_num = getSents($gold_fp, \@gold_sents);
my $tmp = getSents($sys_fp, \@sys_sents);

if($sent_num != $tmp){
    die "different number of sentences: $sent_num in $ARGV[0] and $tmp in $ARGV[1].\n";
}

my $gold_word_num = 0;
my $suc_word_num = 0;     ## num of words in suc_sents
my $match_word_num = 0;   ## num of words in suc_sents with the same tags as in gold standard

my $suc_sent = 0;
my $untagged_sent = 0;
my $leng_mismatch_sent = 0;
my $wrong_format_sent = 0;

my $num_patt = '\d+(\.\d+)?(e\-?\d+)?|e\^\-?\d+\.?\d+?';

for(my $i=0; $i<$sent_num; $i++){
    my $gold_sent = $gold_sents[$i];
    my $sys_sent = $sys_sents[$i];
    
    $gold_sent =~ s/\s+($num_patt)\s*$//;
    $sys_sent =~ s/\s+($num_patt)\s*$//;

    my @gold_tokens = split(/\s+/, $gold_sent);
    my @sys_tokens = split(/\s+/, $sys_sent);

    my $sent_leng = scalar @gold_tokens;
    $gold_word_num += $sent_leng;

    if($sys_sent =~ /^\s*$/ || $sys_sent =~ /^\s*0\s*$/){
	print STDERR "System did not tag the sentence +$gold_sent+\n";
	$untagged_sent ++;
	next;
    }
    

    my $t = scalar @sys_tokens;
    if($sent_leng != $t){
	print STDERR "leng mismatch:\n num=$sent_leng: +$gold_sent+\n num=$t: +$sys_sent+\n";
	$leng_mismatch_sent ++;
	next;
    }

   
    my @gold_tags = ();
    my @sys_tags = ();

    my $suc = getTagSeq(\@gold_tokens, \@gold_tags);
    if(!$suc){
	$wrong_format_sent ++;
	next;
    }

    $suc = getTagSeq(\@sys_tokens, \@sys_tags);
    if(!$suc){
	$wrong_format_sent ++;
	next;
    }

    $suc_sent ++;
    $suc_word_num += $sent_leng;

    for(my $i=0; $i<$sent_leng; $i++){
	if($sys_tags[$i] eq $gold_tags[$i]){
	    $match_word_num ++;
	}
    }
}


my $all_sent = $suc_sent + $untagged_sent + $leng_mismatch_sent + $wrong_format_sent;
my $t3 = ($untagged_sent*100.0)/$all_sent;
print STDERR "sent_num: counted_sent=$suc_sent untagged=$untagged_sent ($t3\%), leng_mismatch=$leng_mismatch_sent wrong_format=$wrong_format_sent\n\n";

print STDERR "word_num: gold=$gold_word_num, counted=$suc_word_num, matched=$match_word_num\n";
my $t1 = ($match_word_num * 100.0)/$gold_word_num;
my $t2 = ($match_word_num * 100.0)/$suc_word_num;
print STDERR "accuracy: overall=$t1\%, among_counted=$t2\% untagged=$t3\%\n";
  
1;



######################
sub getTagSeq {
    my ($tokens_ptr, $tags_ptr) = @_;

    @$tags_ptr = ();

    my $tag = "";

    foreach my $token (@$tokens_ptr){
	my $suc = getTag($token, \$tag);
	if(!$suc){
	    return 0;
	}

	push(@$tags_ptr, $tag);
    }

    return 1;
}



sub getTag {
    my ($token, $tag_ptr) = @_;

    if($token =~ /$delim([^$delim]+)$/){
	$$tag_ptr = $1;
	return 1;
    }else{
	print STDERR "wrong format: +$token+\n";
	return 0;
    }
}


sub getSents {
    my ($fp, $sents_ptr) = @_;

    @$sents_ptr = ();

    while(<$fp>){
	chomp;
	if(/^\s*$/){
	    next;
	}

	s/^\s+//;
	s/\s+$//g;
	push(@$sents_ptr, $_);
    }

    return scalar @$sents_ptr;
}
