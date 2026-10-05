import DatasetDetail from "@/components/DatasetDetail";

export function generateStaticParams() {
  return [
    { slug: "contratos_electronicos_obra" },
    { slug: "procesos_contratacion_obra" },
    { slug: "adiciones_obra" },
    { slug: "proveedores_obra" },
    { slug: "proponentes_por_proceso_obra" },
    { slug: "contratos_adiciones_obra" },
    { slug: "proveedores_rup" },
  ];
}

export default async function Page({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  return <DatasetDetail slug={slug} />;
}
