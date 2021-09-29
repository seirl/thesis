$pdf_mode = 4;  # lualatex
$lualatex = 'lualatex -shell-escape %O %S';
$postscript_mode = $dvi_mode = 0;
$bibtex_use = 2;
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
