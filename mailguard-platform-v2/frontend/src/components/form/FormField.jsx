// Nje fushe formulari: etiketa ("From date") siper dhe kontrolli (input/select) poshte.
// Perdoret ne Search, Reports dhe Import/Export qe te mos perserisim <label> kudo.
function FormField({ label, children, className = "" }) {
  return (
    <div className={className}>
      <label className="form-label">{label}</label>
      {children}
    </div>
  );
}

export default FormField;
