$pdf_mode = 5;  # xelatex
$xelatex = 'xelatex -shell-escape %O %S';
$bibtex_use = 1;
$out_dir = "_build";

# Glossaries

add_cus_dep( 'acn', 'acr', 0, 'makeglossaries' );
add_cus_dep( 'glo', 'gls', 0, 'makeglossaries' );
$clean_ext .= " acr acn alg glo gls glg";
sub makeglossaries {
  my ($base_name, $path) = fileparse( $_[0] );
  pushd $path;
  my $return = system "makeglossaries", $base_name;
  popd;
  return $return;
}
